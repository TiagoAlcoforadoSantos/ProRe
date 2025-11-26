"""
Material model - Waste materials published by producers for recycling.
"""
from datetime import datetime
from enum import Enum
from extensions import db


class StatusMaterial(str, Enum):
    """Material review status enumeration."""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


class CategoriaMaterial(str, Enum):
    """Material category enumeration."""
    PLASTICO = 'plastico'
    VIDRO = 'vidro'
    PAPEL = 'papel'
    METAL = 'metal'
    ELETRONICOS = 'eletronicos'
    ORGANICO = 'organico'


class Material(db.Model):
    """
    Material model - represents waste materials published by producers.
    """
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    localizacao = db.Column(db.String(300), nullable=False)
    quantidade = db.Column(db.String(100), nullable=True)

    # Status and review
    status = db.Column(db.String(20), default=StatusMaterial.PENDING.value, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    pontos_concedidos = db.Column(db.Integer, default=0, nullable=False)

    # Relationships
    produtor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curador_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    revisado_em = db.Column(db.DateTime, nullable=True)

    # Relationships
    produtor = db.relationship('User', foreign_keys=[produtor_id], backref='materiais_publicados')
    curador = db.relationship('User', foreign_keys=[curador_id], backref='materiais_revisados')

    def __repr__(self):
        return f'<Material {self.nome} ({self.status})>'

    def get_categoria_display(self):
        """Return human-readable category name."""
        categoria_map = {
            CategoriaMaterial.PLASTICO.value: 'Plástico',
            CategoriaMaterial.VIDRO.value: 'Vidro',
            CategoriaMaterial.PAPEL.value: 'Papel',
            CategoriaMaterial.METAL.value: 'Metal',
            CategoriaMaterial.ELETRONICOS.value: 'Eletrônicos',
            CategoriaMaterial.ORGANICO.value: 'Orgânico'
        }
        return categoria_map.get(self.categoria, self.categoria.capitalize())

    def get_status_display(self):
        """Return human-readable status name."""
        status_map = {
            StatusMaterial.PENDING.value: 'Aguardando',
            StatusMaterial.APPROVED.value: 'Aprovado',
            StatusMaterial.REJECTED.value: 'Reprovado'
        }
        return status_map.get(self.status, 'Desconhecido')

    def to_dict(self):
        """Convert material to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'name': self.nome,
            'category': self.get_categoria_display(),
            'category_value': self.categoria,
            'description': self.descricao,
            'location': self.localizacao,
            'quantity': self.quantidade,
            'status': self.status,
            'status_display': self.get_status_display(),
            'feedback': self.feedback,
            'points': self.pontos_concedidos,
            'producer': self.produtor.get_full_name() if self.produtor else None,
            'producer_id': self.produtor_id,
            'curator_id': self.curador_id,
            'date': self.criado_em.strftime('%d/%m/%Y') if self.criado_em else None,
            'reviewed_date': self.revisado_em.strftime('%d/%m/%Y') if self.revisado_em else None
        }
