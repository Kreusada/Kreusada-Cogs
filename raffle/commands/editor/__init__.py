from .allowed import Allowed
from .badges import Badges
from .editor import EditorCommands as Editor
from .prevented import Prevented
from .role_requirements import RoleRequirements
from ...mixins.metaclass import MetaClass

mixins = (Allowed, Badges, Prevented, RoleRequirements, Editor)


class EditorCommands(*mixins, metaclass=MetaClass):
    pass
