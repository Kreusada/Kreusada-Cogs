import asyncio
import datetime
from random import shuffle
from typing import KeysView, Optional, TYPE_CHECKING, ValuesView

import discord
from discord.backoff import ExponentialBackoff

from . import log, ws_rll_log
from .enums import *
from .rest_api import RESTClient, Track

if TYPE_CHECKING:
    from . import node

__all__ = ["user_id", "channel_finder_func", "Player", "PlayerManager"]

user_id = None
channel_finder_func = lambda channel_id: None


class Player(RESTClient):
    """
    The Player class represents the current state of playback.
    It also is used to control playback and queue tracks.

    The existence of this object guarantees that the bot is connected
    to a voice channel.

    Attributes
    ----------
    channel: discord.VoiceChannel
        The channel the bot is connected to.
    queue : list of Track
    position : int
        The seeked position in the track of the current playback.
    current : Track
    repeat : bool
    shuffle : bool
    """

    def __init__(self, manager: "PlayerManager", channel: discord.VoiceChannel):
        super().__init__(manager.node)
        self.bot = manager.bot
        self.channel = channel
        self.guild = channel.guild
        self._last_channel_id = channel.id
        self.queue = []
        self.position = 0
        self.current = None  # type: Track
        self._paused = False
        self.repeat = False
        self.shuffle = False  # Shuffle is done client side now This is a breaking change
        self.shuffle_bumped = True
        self._is_autoplaying = False
        self._auto_play_sent = False
        self._volume = 100
        self.state = PlayerState.CREATED
        self.connected_at = None
        self._connected = False

        self._is_playing = False
        self._metadata = {}
        self.manager = manager
        self._con_delay = None
        self._last_resume = None

    def __repr__(self):
        return (
            "<Player: "
            f"state={self.state.name}, connected={self.connected}, "
            f"guild={self.guild.name!r} ({self.guild.id}), "
            f"channel={self.channel.name!r} ({self.channel.id}), "
            f"playing={self.is_playing}, paused={self.paused}, volume={self.volume}, "
            f"queue_size={len(self.queue)}, current={self.current!r}, "
            f"position={self.position}, "
            f"length={self.current.length if self.current else 0}, node={self.node!r}>"
        )

    @property
    def is_auto_playing(self) -> bool:
        """
        Current status of playback
        """
        return self._is_playing and not self._paused and self._is_autoplaying

    @property
    def is_playing(self) -> bool:
        """
        Current status of playback
        """
        return self._is_playing and not self._paused and self._connected

    @property
    def paused(self) -> bool:
        """
        Player's paused state.
        """
        return self._paused

    @property
    def volume(self) -> int:
        """
        The current volume.
        """
        return self._volume

    @property
    def ready(self) -> bool:
        """
        Whether the underlying node is ready for requests.
        """
        return self.node.ready

    @property
    def connected(self) -> bool:
        """
        Whether the player is ready to be used.
        """
        return self._connected

    async def wait_until_ready(
        self, timeout: Optional[float] = None, no_raise: bool = False
    ) -> bool:
        """
        Waits for the underlying node to become ready.

        If no_raise is set, returns false when a timeout occurs instead of propogating TimeoutError.
        A timeout of None means to wait indefinitely.
        """
        if self.node.ready:
            return True

        try:
            return await self.node.wait_until_ready(timeout=timeout)
        except asyncio.TimeoutError:
            if no_raise:
                return False
            else:
                raise

    async def connect(self, deafen: bool = False, channel: Optional[discord.VoiceChannel] = None):
        """
        Connects to the voice channel associated with this Player.
        """
        self._last_resume = datetime.datetime.now(tz=datetime.timezone.utc)
        self.connected_at = datetime.datetime.now(datetime.timezone.utc)
        self._connected = True
        if channel:
            if self.channel:
                self._last_channel_id = self.channel.id
            self.channel = channel
        await self.guild.change_voice_state(
            channel=self.channel, self_mute=False, self_deaf=deafen
        )

    async def move_to(self, channel: discord.VoiceChannel, deafen: bool = False):
        """
        Moves this player to a voice channel.

        Parameters
        ----------
        channel : discord.VoiceChannel
        """
        if channel.guild != self.guild:
            raise TypeError(f"Cannot move {self!r} to a different guild.")
        if self.channel:
            self._last_channel_id = self.channel.id
        self.channel = channel
        await self.connect(deafen=deafen)
        if self.current:
            await self.resume(
                track=self.current, replace=True, start=self.position, pause=self._paused
            )

    async def disconnect(self, requested=True):
        """
        Disconnects this player from it's voice channel.
        """
        self._is_autoplaying = False
        self._auto_play_sent = False
        self._connected = False
        if self.state == PlayerState.DISCONNECTING:
            return

        await self.update_state(PlayerState.DISCONNECTING)
        guild_id = self.guild.id
        if not requested:
            log.debug("Forcing player disconnect for %r due to player manager request.", self)
            self.node.event_handler(
                LavalinkIncomingOp.EVENT,
                LavalinkEvents.FORCED_DISCONNECT,
                {
                    "guildId": guild_id,
                    "code": 42069,
                    "reason": "Forced Disconnect - Do not Reconnect",
                    "byRemote": True,
                    "retries": -1,
                },
            )

        voice_ws = self.node.get_voice_ws(guild_id)

        if not voice_ws.socket.closed:
            await self.guild.change_voice_state(channel=None)

        await self.node.destroy_guild(guild_id)
        await self.close()

        self.manager.remove_player(self)

    def store(self, key, value):
        """
        Stores a metadata value by key.
        """
        self._metadata[key] = value

    def fetch(self, key, default=None):
        """
        Returns a stored metadata value.

        Parameters
        ----------
        key
            Key used to store metadata.
        default
            Optional, used if the key doesn't exist.
        """
        return self._metadata.get(key, default)

    async def update_state(self, state: PlayerState):
        if state == self.state:
            return

        ws_rll_log.debug("Player %r changing state: %s -> %s", self, self.state.name, state.name)

        old_state = self.state
        self.state = state

        if self._con_delay:
            self._con_delay = None

        if state == PlayerState.READY:
            self.reset_session()

    async def handle_event(self, event: "node.LavalinkEvents", extra):
        """
        Handles various Lavalink Events.

        If the event is TRACK END, extra will be TrackEndReason.

        If the event is TRACK EXCEPTION, extra will be the string reason.

        If the event is TRACK STUCK, extra will be the threshold ms.

        Parameters
        ----------
        event : node.LavalinkEvents
        extra
        """
        log.debug("Received player event for player: %r - %r - %r.", self, event, extra)

        if event == LavalinkEvents.TRACK_END:
            if extra == TrackEndReason.FINISHED:
                await self.play()
            else:
                self._is_playing = False
        elif event == LavalinkEvents.WEBSOCKET_CLOSED:
            code = extra.get("code")
            if code in (4015, 4014, 4009, 4006, 4000, 1006):
                if not self._con_delay:
                    self._con_delay = ExponentialBackoff(base=1)

    async def handle_player_update(self, state: "node.PlayerState"):
        """
        Handles player updates from lavalink.

        Parameters
        ----------
        state : websocket.PlayerState
        """
        if state.position > self.position:
            self._is_playing = True
        log.debug("Updated player position for player: %r - %ds.", self, state.position // 1000)
        self.position = state.position

    # Play commands
    def add(self, requester: discord.User, track: Track):
        """
        Adds a track to the queue.

        Parameters
        ----------
        requester : discord.User
            User who requested the track.
        track : Track
            Result from any of the lavalink track search methods.
        """
        track.requester = requester
        self.queue.append(track)

    def maybe_shuffle(self, sticky_songs: int = 1):
        if self.shuffle and self.queue:  # Keeps queue order consistent unless adding new tracks
            self.force_shuffle(sticky_songs)

    def force_shuffle(self, sticky_songs: int = 1):
        if not self.queue:
            return
        sticky = max(0, sticky_songs)  # Songs to  bypass shuffle
        # Keeps queue order consistent unless adding new tracks
        if sticky > 0:
            to_keep = self.queue[:sticky]
            to_shuffle = self.queue[sticky:]
        else:
            to_shuffle = self.queue
            to_keep = []
        if not self.shuffle_bumped:
            to_keep_bumped = [t for t in to_shuffle if t.extras.get("bumped", None)]
            to_shuffle = [t for t in to_shuffle if not t.extras.get("bumped", None)]
            to_keep.extend(to_keep_bumped)
            # Shuffles whole queue
        shuffle(to_shuffle)
        to_keep.extend(to_shuffle)
        # Keep next track in queue consistent while adding new tracks
        self.queue = to_keep

    async def play(self):
        """
        Starts playback from lavalink.
        """
        if self.repeat and self.current is not None:
            self.queue.append(self.current)

        self.current = None
        self.position = 0
        self._paused = False

        if not self.queue:
            await self.stop()
        else:
            self._is_playing = True

            track = self.queue.pop(0)

            self.current = track
            log.debug("Assigned current track for player: %r.", self)
            await self.node.play(self.guild.id, track, start=track.start_timestamp, replace=True)

    async def resume(
        self, track: Track, replace: bool = True, start: int = 0, pause: bool = False
    ):
        log.debug("Resuming current track for player: %r.", self)
        self._is_playing = False
        self._paused = True
        await self.node.play(self.guild.id, track, start=start, replace=replace, pause=True)
        await self.pause(True)
        await self.pause(pause, timed=1)

    async def stop(self):
        """
        Stops playback from lavalink.

        .. important::

            This method will clear the queue.
        """
        await self.node.stop(self.guild.id)
        self.queue = []
        self.current = None
        self.position = 0
        self._paused = False
        self._is_autoplaying = False
        self._auto_play_sent = False

    async def skip(self):
        """
        Skips to the next song.
        """
        await self.play()

    async def pause(self, pause: bool = True, timed: Optional[int] = None):
        """
        Pauses the current song.

        Parameters
        ----------
        pause : bool
            Set to ``False`` to resume.
        timed : Optional[int]
            If an int is given the op will be called after it.
        """
        if timed is not None:
            await asyncio.sleep(timed)

        self._paused = pause
        await self.node.pause(self.guild.id, pause)

    async def set_volume(self, volume: int):
        """
        Sets the volume of Lavalink.

        Parameters
        ----------
        volume : int
            Between 0 and 150
        """
        self._volume = max(min(volume, 150), 0)
        await self.node.volume(self.guild.id, self.volume)

    async def seek(self, position: int):
        """
        If the track allows it, seeks to a position.

        Parameters
        ----------
        position : int
            Between 0 and track length.
        """
        if self.current.seekable:
            position = max(min(position, self.current.length), 0)
            await self.node.seek(self.guild.id, position)


class PlayerManager:
    def __init__(self, node_: "node.Node"):
        self._player_dict = {}
        self.voice_states = {}
        self.bot = node_.bot
        self.node = node_
        self.node.register_state_handler(self.node_state_handler)

    @property
    def players(self) -> ValuesView[Player]:
        return self._player_dict.values()

    @property
    def guild_ids(self) -> KeysView[int]:
        return self._player_dict.keys()

    async def create_player(self, channel: discord.VoiceChannel, deafen: bool = False) -> Player:
        """
        Connects to a discord voice channel.

        This function is safe to repeatedly call as it will return an existing
        player if there is one.

        Parameters
        ----------
        channel

        Returns
        -------
        Player
            The created Player object.
        """
        if self._already_in_guild(channel):
            p = self.get_player(channel.guild.id)
            await p.move_to(channel, deafen=deafen)
        else:
            p = Player(self, channel)
            await p.connect(deafen=deafen)
            self._player_dict[channel.guild.id] = p
            await self.refresh_player_state(p)
        return p

    def _already_in_guild(self, channel: discord.VoiceChannel) -> bool:
        return channel.guild.id in self._player_dict

    def get_player(self, guild_id: int) -> Player:
        """
        Gets a Player object from a guild ID.

        Parameters
        ----------
        guild_id : int
            Discord guild ID.

        Returns
        -------
        Player

        Raises
        ------
        KeyError
            If that guild does not have a Player, e.g. is not connected to any
            voice channel.
        """
        if guild_id in self._player_dict:
            return self._player_dict[guild_id]
        raise KeyError("No such player for that guild.")

    def _ensure_player(self, channel_id: int):
        channel = channel_finder_func(channel_id)
        if channel is not None:
            try:
                p = self.get_player(channel.guild.id)
            except KeyError:
                log.debug("Received voice channel connection without a player.")
                p = Player(self, channel)
                self._player_dict[channel.guild.id] = p
            return p, channel

    async def _remove_player(self, guild_id: int):
        try:
            p = self.get_player(guild_id)
        except KeyError:
            pass
        else:
            del self._player_dict[guild_id]
            await p.disconnect(requested=False)

    async def node_state_handler(self, next_state: NodeState, old_state: NodeState):
        ws_rll_log.debug("Received node state update: %s -> %s", old_state.name, next_state.name)
        if next_state == NodeState.READY:
            await self.update_player_states(PlayerState.READY)
        elif next_state == NodeState.DISCONNECTING:
            await self.update_player_states(PlayerState.DISCONNECTING)
        elif next_state in (NodeState.CONNECTING, NodeState.RECONNECTING):
            await self.update_player_states(PlayerState.NODE_BUSY)

    async def update_player_states(self, state: PlayerState):
        for p in self.players:
            await p.update_state(state)

    async def refresh_player_state(self, player: Player):
        if self.node.ready:
            await player.update_state(PlayerState.READY)
        elif self.node.state == NodeState.DISCONNECTING:
            await player.update_state(PlayerState.DISCONNECTING)
        else:
            await player.update_state(PlayerState.NODE_BUSY)

    async def on_socket_response(self, data):
        raw_event = data.get("t")
        try:
            event = DiscordVoiceSocketResponses(raw_event)
        except ValueError:
            return

        guild_id = data["d"]["guild_id"]
        if guild_id not in self.voice_states:
            self.voice_states[guild_id] = {}

        if event == DiscordVoiceSocketResponses.VOICE_SERVER_UPDATE:
            # Connected for the first time
            socket_event_data = data["d"]
            self.voice_states[guild_id].update({"guild_id": guild_id, "event": socket_event_data})
        elif event == DiscordVoiceSocketResponses.VOICE_STATE_UPDATE:
            channel_id = data["d"]["channel_id"]
            event_user_id = int(data["d"].get("user_id"))

            if event_user_id != user_id:
                return

            if channel_id is None:
                # We disconnected
                p = self._player_dict.get(guild_id)
                msg = "Received voice disconnect from discord, removing player."
                if p:
                    msg += f" {p}"
                ws_rll_log.info(msg)
                self.voice_states[guild_id] = {}
                await self._remove_player(int(guild_id))

            else:
                # After initial connection, get session ID
                p, channel = self._ensure_player(int(channel_id))
                if channel != p.channel:
                    if p.channel:
                        p._last_channel_id = p.channel.id
                    p.channel = channel

            session_id = data["d"]["session_id"]
            self.voice_states[guild_id]["session_id"] = session_id
        else:
            return
        data = self.voice_states[guild_id]
        if all(k in data for k in ["session_id", "guild_id", "event"]):
            await self.node.send_lavalink_voice_update(**self.voice_states[guild_id])

    async def disconnect(self):
        """
        Disconnects all players.
        """
        for p in tuple(self.players):
            await p.disconnect(requested=False)
        log.debug("Disconnected all players.")

    def remove_player(self, player: Player):
        if player.state != PlayerState.DISCONNECTING:
            log.error(
                "Attempting to remove a player (%r) from player list with state: %s",
                player,
                player.state.name,
            )
            return
        guild_id = player.channel.guild.id
        if guild_id in self._player_dict:
            del self._player_dict[guild_id]
