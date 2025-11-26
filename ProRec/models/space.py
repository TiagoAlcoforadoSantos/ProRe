"""
Space model - Physical spaces for collection points and events.
"""
from datetime import datetime
from enum import Enum
from extensions import db


class TipoEspaco(str, Enum):
    """Space type enumeration."""
    COLETA = 'coleta'
    EVENTO = 'evento'
    CURSO = 'curso'


class Space(db.Model):
    """
    Space model - represents physical collection points and event venues.
    """
    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), default=TipoEspaco.COLETA.value, nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    horario = db.Column(db.String(100), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    # Optional coordinates for map
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    eventos = db.relationship('Event', back_populates='espaco', lazy='dynamic')

    def __repr__(self):
        return f'<Space {self.nome} ({self.tipo})>'

    def get_tipo_display(self):
        """Return human-readable type name."""
        tipo_map = {
            TipoEspaco.COLETA.value: 'Coleta',
            TipoEspaco.EVENTO.value: 'Evento',
            TipoEspaco.CURSO.value: 'Curso'
        }
        return tipo_map.get(self.tipo, 'Desconhecido')

    def to_dict(self):
        """Convert space to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.nome,
            'type': self.tipo,
            'type_display': self.get_tipo_display(),
            'address': self.endereco,
            'hours': self.horario,
            'description': self.descricao,
            'active': self.ativo,
            'latitude': self.latitude,
            'longitude': self.longitude
        }
