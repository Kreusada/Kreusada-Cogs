from ..mixins.metaclass import MetaClass
from .builder import BuilderCommands
from .editor import EditorCommands
from .events import EventCommands
from .informational import InformationalCommands
from .misc import MiscCommands

mixins = (
    BuilderCommands,
    EventCommands,
    EditorCommands,
    InformationalCommands,
    MiscCommands,
)


class Commands(*mixins, metaclass=MetaClass):
    """Mixin used for command-based mixin classes"""
