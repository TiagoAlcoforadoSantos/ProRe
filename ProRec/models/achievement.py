"""
Achievement model - Gamification achievements for producers.
"""
from datetime import datetime
from extensions import db


class Achievement(db.Model):
    """
    Achievement model - represents available achievements/badges.
    """
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    icone = db.Column(db.String(10), nullable=False)  # Emoji icon
    pontos_necessarios = db.Column(db.Integer, default=0, nullable=False)
    ordem = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<Achievement {self.nome}>'

    def to_dict(self, user_points=0):
        """Convert achievement to dictionary for JSON serialization."""
        unlocked = user_points >= self.pontos_necessarios
        points_remaining = max(0, self.pontos_necessarios - user_points)
        return {
            'id': self.id,
            'name': self.nome,
            'description': self.descricao,
            'icon': self.icone,
            'points_required': self.pontos_necessarios,
            'unlocked': unlocked,
            'points_remaining': points_remaining
        }


class Collection(db.Model):
    """
    Collection model - records of completed material collections.
    """
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    material_nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.String(100), nullable=True)
    pontos = db.Column(db.Integer, default=0, nullable=False)
    feedback = db.Column(db.Text, nullable=True)

    # Relationships
    produtor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=True)

    # Timestamps
    data_coleta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    produtor = db.relationship('User', backref='coletas')
    material = db.relationship('Material', backref='coleta')

    def __repr__(self):
        return f'<Collection {self.material_nome} - {self.pontos} pts>'

    def get_categoria_display(self):
        """Return human-readable category name."""
        categoria_map = {
            'plastico': 'Plástico',
            'vidro': 'Vidro',
            'papel': 'Papel',
            'metal': 'Metal',
            'eletronicos': 'Eletrônicos',
            'organico': 'Orgânico'
        }
        return categoria_map.get(self.categoria, self.categoria.capitalize())

    def to_dict(self):
        """Convert collection to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'material_name': self.material_nome,
            'category': self.get_categoria_display(),
            'category_value': self.categoria,
            'quantity': self.quantidade,
            'points': self.pontos,
            'feedback': self.feedback,
            'date': self.data_coleta.strftime('%Y-%m-%d') if self.data_coleta else None
        }
