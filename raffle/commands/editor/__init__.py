from ...mixins.metaclass import MetaClass
from .allowed import Allowed
from .badges import Badges
from .main import EditorCommands as Editor
from .prevented import Prevented
from .role_requirements import RoleRequirements

mixins = (Allowed, Badges, Prevented, RoleRequirements, Editor)


class EditorCommands(*mixins, metaclass=MetaClass):
    pass
