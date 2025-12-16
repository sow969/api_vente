from .userController import api as user_ns
from .profilController import api as profil_ns


def register_resources(api):
    api.add_namespace(user_ns, path='/users')
    api.add_namespace(profil_ns, path='/profils')
