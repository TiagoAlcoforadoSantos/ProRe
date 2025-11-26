"""
Models package initialization.
Import all models here for easier access.
"""
from models.user import User, TipoUsuario, StatusUsuario, Notificacao, TipoNotificacao
from models.material import Material, StatusMaterial, CategoriaMaterial
from models.space import Space, TipoEspaco
from models.event import Event, TipoEvento, StatusEvento
from models.achievement import Achievement, Collection

__all__ = [
    'User', 'TipoUsuario', 'StatusUsuario', 'Notificacao', 'TipoNotificacao',
    'Material', 'StatusMaterial', 'CategoriaMaterial',
    'Space', 'TipoEspaco',
    'Event', 'TipoEvento', 'StatusEvento',
    'Achievement', 'Collection'
]
