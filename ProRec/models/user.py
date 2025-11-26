"""
User model - Migrated from Django CustomUser.
"""
from datetime import datetime
from enum import Enum
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class TipoUsuario(int, Enum):
    """User type enumeration."""
    ADMIN = 1
    CURATOR = 2
    PRODUCER = 3


class StatusUsuario(str, Enum):
    """User status enumeration."""
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    PENDENTE = 'pendente'


class User(UserMixin, db.Model):
    """
    User model - equivalent to Django's CustomUser.
    Extends AbstractUser fields with custom tipo, status, and pontos.
    """
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Authentication fields (from AbstractUser)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile fields (from AbstractUser)
    first_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)

    # Custom fields
    tipo = db.Column(db.Integer, default=TipoUsuario.PRODUCER.value, nullable=False)
    status = db.Column(db.String(10), default=StatusUsuario.PENDENTE.value, nullable=False)
    pontos = db.Column(db.Integer, default=0, nullable=False)

    # Timestamps
    date_joined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ultima_atividade = db.Column(db.DateTime, default=datetime.utcnow,
                                  onupdate=datetime.utcnow, nullable=False)

    # Relationships (will be added as we create other models)
    notificacoes = db.relationship('Notificacao', back_populates='usuario',
                                   lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username} ({self.get_tipo_display()})>'

    def get_full_name(self):
        """Return the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_tipo_display(self):
        """Return human-readable tipo name."""
        tipo_map = {
            TipoUsuario.ADMIN.value: 'Administrador',
            TipoUsuario.CURATOR.value: 'Curador',
            TipoUsuario.PRODUCER.value: 'Produtor'
        }
        return tipo_map.get(self.tipo, 'Desconhecido')

    def get_status_display(self):
        """Return human-readable status name."""
        status_map = {
            StatusUsuario.ATIVO.value: 'Ativo',
            StatusUsuario.INATIVO.value: 'Inativo',
            StatusUsuario.PENDENTE.value: 'Pendente'
        }
        return status_map.get(self.status, 'Desconhecido')

    # Password management
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password."""
        return check_password_hash(self.password_hash, password)

    # Role checking methods (from Django CustomUser)
    def is_admin(self):
        """Check if user is an administrator."""
        return self.tipo == TipoUsuario.ADMIN.value

    def is_curator(self):
        """Check if user is a curator."""
        return self.tipo == TipoUsuario.CURATOR.value

    def is_producer(self):
        """Check if user is a producer."""
        return self.tipo == TipoUsuario.PRODUCER.value

    # Status checking methods
    def is_ativo(self):
        """Check if user status is active."""
        return self.status == StatusUsuario.ATIVO.value

    def is_pendente(self):
        """Check if user status is pending."""
        return self.status == StatusUsuario.PENDENTE.value

    # Flask-Login required properties
    def get_id(self):
        """Return the user ID as a string (required by Flask-Login)."""
        return str(self.id)

    @property
    def is_authenticated(self):
        """Always True for authenticated users."""
        return True

    @property
    def is_anonymous(self):
        """Always False for real users."""
        return False

    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nome': self.get_full_name(),
            'tipo': self.tipo,
            'tipo_display': self.get_tipo_display(),
            'status': self.status,
            'status_display': self.get_status_display(),
            'pontos': self.pontos,
            'ultima_atividade': self.ultima_atividade.isoformat() if self.ultima_atividade else None
        }


class TipoNotificacao(str, Enum):
    """Notification type enumeration."""
    INFO = 'info'
    ACHIEVEMENT = 'achievement'
    REMINDER = 'reminder'


class Notificacao(db.Model):
    """
    Notification model for users.
    Migrated from Django Notificacao model.
    """
    __tablename__ = 'notificacoes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    lida = db.Column(db.Boolean, default=False, nullable=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    usuario = db.relationship('User', back_populates='notificacoes')

    class Meta:
        ordering = ['-criada_em']

    def __repr__(self):
        return f'<Notificacao {self.titulo} - {self.usuario.username}>'

    def get_tipo_display(self):
        """Return human-readable notification type."""
        tipo_map = {
            TipoNotificacao.INFO.value: 'Informação',
            TipoNotificacao.ACHIEVEMENT.value: 'Conquista',
            TipoNotificacao.REMINDER.value: 'Lembrete'
        }
        return tipo_map.get(self.tipo, 'Desconhecido')

    def to_dict(self):
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'tipo_display': self.get_tipo_display(),
            'titulo': self.titulo,
            'mensagem': self.mensagem,
            'lida': self.lida,
            'criada_em': self.criada_em.isoformat()
        }
