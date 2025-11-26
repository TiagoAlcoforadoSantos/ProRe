"""
Event model - Events and activities related to recycling.
"""
from datetime import datetime
from enum import Enum
from extensions import db


class TipoEvento(str, Enum):
    """Event type enumeration."""
    COLETA = 'coleta'
    EVENTO = 'evento'
    CURSO = 'curso'
    WORKSHOP = 'workshop'


class StatusEvento(str, Enum):
    """Event status enumeration."""
    AGENDADO = 'agendado'
    EM_ANDAMENTO = 'em_andamento'
    CONCLUIDO = 'concluido'
    CANCELADO = 'cancelado'


class Event(db.Model):
    """
    Event model - represents scheduled recycling events and activities.
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(20), default=TipoEvento.COLETA.value, nullable=False)
    status = db.Column(db.String(20), default=StatusEvento.AGENDADO.value, nullable=False)

    # Schedule
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=True)
    horario = db.Column(db.String(50), nullable=True)

    # Location (can be linked to a space or have custom location)
    espaco_id = db.Column(db.Integer, db.ForeignKey('spaces.id'), nullable=True)
    localizacao_custom = db.Column(db.String(300), nullable=True)

    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    espaco = db.relationship('Space', back_populates='eventos')

    def __repr__(self):
        return f'<Event {self.titulo} ({self.tipo})>'

    def get_tipo_display(self):
        """Return human-readable type name."""
        tipo_map = {
            TipoEvento.COLETA.value: 'Coleta',
            TipoEvento.EVENTO.value: 'Evento',
            TipoEvento.CURSO.value: 'Curso',
            TipoEvento.WORKSHOP.value: 'Workshop'
        }
        return tipo_map.get(self.tipo, 'Desconhecido')

    def get_status_display(self):
        """Return human-readable status name."""
        status_map = {
            StatusEvento.AGENDADO.value: 'Programado',
            StatusEvento.EM_ANDAMENTO.value: 'Em andamento',
            StatusEvento.CONCLUIDO.value: 'Concluído',
            StatusEvento.CANCELADO.value: 'Cancelado'
        }
        return status_map.get(self.status, 'Desconhecido')

    def get_localizacao(self):
        """Return event location (from space or custom)."""
        if self.espaco:
            return self.espaco.nome
        return self.localizacao_custom or 'Local não definido'

    def to_dict(self):
        """Convert event to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.titulo,
            'description': self.descricao,
            'type': self.tipo,
            'type_display': self.get_tipo_display(),
            'status': self.status,
            'status_display': self.get_status_display(),
            'date': self.data_inicio.strftime('%d %b %Y') if self.data_inicio else None,
            'date_iso': self.data_inicio.isoformat() if self.data_inicio else None,
            'time': self.horario,
            'location': self.get_localizacao(),
            'space_id': self.espaco_id
        }
