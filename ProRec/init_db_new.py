"""
Database initialization script for ProRec Flask application.
Creates tables and seed data with test users matching the Django implementation.
"""
from datetime import datetime, timedelta
from app import create_app
from extensions import db
from models.user import User, TipoUsuario, StatusUsuario
from models.material import Material, StatusMaterial
from models.space import Space, TipoEspaco
from models.event import Event, TipoEvento, StatusEvento
from models.achievement import Achievement, Collection

def init_database():
    """Initialize database with tables and seed data."""
    app = create_app('development')

    with app.app_context():
        # Show the database location for debugging
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        print(f"Database location: {db_uri.replace('sqlite:///', '')}")
        print("Creating database tables...")
        db.create_all()

        # Check if users already exist
        if User.query.count() > 0:
            print("Database already initialized. Skipping seed data.")
            return

        print("Creating test users...")

        # Create Admin user
        admin = User(
            username='admin@reciclo.com',
            email='admin@reciclo.com',
            first_name='Administrador',
            last_name='Sistema',
            tipo=TipoUsuario.ADMIN.value,
            status=StatusUsuario.ATIVO.value,
            is_active=True,
            is_staff=True,
            is_superuser=True
        )
        admin.set_password('senha123')
        db.session.add(admin)

        # Create Curator user
        curator = User(
            username='curador@reciclo.com',
            email='curador@reciclo.com',
            first_name='Curador',
            last_name='Teste',
            tipo=TipoUsuario.CURATOR.value,
            status=StatusUsuario.ATIVO.value,
            is_active=True
        )
        curator.set_password('senha123')
        db.session.add(curator)

        # Create Producer user
        producer = User(
            username='produtor@reciclo.com',
            email='produtor@reciclo.com',
            first_name='Produtor',
            last_name='Teste',
            tipo=TipoUsuario.PRODUCER.value,
            status=StatusUsuario.ATIVO.value,
            pontos=370,
            is_active=True
        )
        producer.set_password('senha123')
        db.session.add(producer)

        # Create pending users for admin approval
        pending_user1 = User(
            username='joao@email.com',
            email='joao@email.com',
            first_name='João',
            last_name='Silva',
            tipo=TipoUsuario.PRODUCER.value,
            status=StatusUsuario.PENDENTE.value,
            is_active=True
        )
        pending_user1.set_password('senha123')
        db.session.add(pending_user1)

        pending_user2 = User(
            username='maria@email.com',
            email='maria@email.com',
            first_name='Maria',
            last_name='Santos',
            tipo=TipoUsuario.PRODUCER.value,
            status=StatusUsuario.PENDENTE.value,
            is_active=True
        )
        pending_user2.set_password('senha123')
        db.session.add(pending_user2)

        # Commit users first to get IDs
        db.session.commit()

        print("Creating achievements...")
        achievements = [
            Achievement(nome='Primeira Coleta', descricao='Realizou sua primeira coleta', icone='🌱', pontos_necessarios=0, ordem=1),
            Achievement(nome='Eco Warrior', descricao='Acumulou 100 pontos', icone='⚡', pontos_necessarios=100, ordem=2),
            Achievement(nome='Guardião Verde', descricao='Acumulou 500 pontos', icone='🌳', pontos_necessarios=500, ordem=3),
            Achievement(nome='Mestre da Reciclagem', descricao='Acumulou 1000 pontos', icone='👑', pontos_necessarios=1000, ordem=4),
        ]
        for achievement in achievements:
            db.session.add(achievement)

        print("Creating spaces...")
        spaces = [
            Space(
                nome='EcoPonto Centro',
                tipo=TipoEspaco.COLETA.value,
                endereco='Rua das Flores, 123 - Centro',
                horario='Seg-Sex: 8h-18h'
            ),
            Space(
                nome='Reciclagem Bairro Norte',
                tipo=TipoEspaco.COLETA.value,
                endereco='Av. Principal, 456 - Norte',
                horario='Seg-Sáb: 7h-19h'
            ),
            Space(
                nome='Centro de Coleta Sul',
                tipo=TipoEspaco.COLETA.value,
                endereco='Rua do Parque, 789 - Sul',
                horario='Seg-Sex: 9h-17h'
            ),
            Space(
                nome='Auditório Sustentabilidade',
                tipo=TipoEspaco.EVENTO.value,
                endereco='Rua das Flores, 500',
                horario='Agendamento prévio'
            ),
            Space(
                nome='Centro de Treinamento',
                tipo=TipoEspaco.CURSO.value,
                endereco='Av. Educação, 300',
                horario='Seg-Sáb: 9h-17h'
            ),
        ]
        for space in spaces:
            db.session.add(space)

        db.session.commit()

        print("Creating events...")
        today = datetime.now()
        events = [
            Event(
                titulo='Coleta de Eletrônicos',
                descricao='Coleta especial de equipamentos eletrônicos',
                tipo=TipoEvento.COLETA.value,
                status=StatusEvento.AGENDADO.value,
                data_inicio=today + timedelta(days=3),
                horario='9:00 - 16:00',
                localizacao_custom='Centro Comunitário'
            ),
            Event(
                titulo='Workshop de Compostagem',
                descricao='Aprenda a fazer compostagem em casa',
                tipo=TipoEvento.WORKSHOP.value,
                status=StatusEvento.AGENDADO.value,
                data_inicio=today + timedelta(days=7),
                horario='14:00 - 17:00',
                localizacao_custom='Praça Central'
            ),
            Event(
                titulo='Feira de Sustentabilidade',
                descricao='Feira com produtos sustentáveis e palestras',
                tipo=TipoEvento.EVENTO.value,
                status=StatusEvento.AGENDADO.value,
                data_inicio=today + timedelta(days=14),
                horario='10:00 - 18:00',
                localizacao_custom='Parque Municipal'
            ),
        ]
        for event in events:
            db.session.add(event)

        print("Creating sample materials...")
        # Get producer ID
        producer = User.query.filter_by(email='produtor@reciclo.com').first()
        curator = User.query.filter_by(email='curador@reciclo.com').first()

        materials = [
            Material(
                nome='Lote de plástico',
                categoria='plastico',
                descricao='10 garrafas PET limpas',
                localizacao='Minha localização',
                quantidade='10 unidades',
                status=StatusMaterial.APPROVED.value,
                produtor_id=producer.id,
                curador_id=curator.id,
                pontos_concedidos=50,
                feedback='Material em excelente estado!',
                revisado_em=datetime.utcnow() - timedelta(days=3)
            ),
            Material(
                nome='Papelão',
                categoria='papel',
                descricao='Caixas desmontadas',
                localizacao='Minha localização',
                quantidade='5kg',
                status=StatusMaterial.PENDING.value,
                produtor_id=producer.id
            ),
            Material(
                nome='Eletrônicos Antigos',
                categoria='eletronicos',
                descricao='Celulares e tablets usados',
                localizacao='Centro da cidade',
                status=StatusMaterial.REJECTED.value,
                produtor_id=producer.id,
                curador_id=curator.id,
                feedback='Por favor, forneça mais detalhes sobre o estado dos aparelhos.',
                revisado_em=datetime.utcnow() - timedelta(days=5)
            ),
        ]
        for material in materials:
            db.session.add(material)

        print("Creating sample collections...")
        collections = [
            Collection(
                material_nome='Garrafas PET',
                categoria='plastico',
                quantidade='50 unidades',
                pontos=150,
                feedback='Excelente qualidade! Material bem separado.',
                produtor_id=producer.id,
                data_coleta=datetime.utcnow() - timedelta(days=10)
            ),
            Collection(
                material_nome='Papelão',
                categoria='papel',
                quantidade='20kg',
                pontos=100,
                feedback='Material em bom estado.',
                produtor_id=producer.id,
                data_coleta=datetime.utcnow() - timedelta(days=15)
            ),
            Collection(
                material_nome='Latas de Alumínio',
                categoria='metal',
                quantidade='30 unidades',
                pontos=120,
                feedback='Ótima contribuição!',
                produtor_id=producer.id,
                data_coleta=datetime.utcnow() - timedelta(days=20)
            ),
        ]
        for collection in collections:
            db.session.add(collection)

        # Commit all data
        db.session.commit()

        print("\n[SUCCESS] Database initialized successfully!")
        print("\nTest Users Created:")
        print("  Admin:    admin@reciclo.com / senha123")
        print("  Curator:  curador@reciclo.com / senha123")
        print("  Producer: produtor@reciclo.com / senha123")
        print("\nSeed Data Created:")
        print("  - 4 Achievements")
        print("  - 5 Spaces (collection points)")
        print("  - 3 Events")
        print("  - 3 Materials (1 approved, 1 pending, 1 rejected)")
        print("  - 3 Collections (history)")
        print("  - 2 Pending users for approval")


if __name__ == '__main__':
    init_database()
