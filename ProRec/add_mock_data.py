"""
Script to add additional mock data to an existing database.
Useful for testing with more data without resetting the database.
"""
from datetime import datetime, timedelta
import random
from app import create_app
from extensions import db
from models.user import User, TipoUsuario, StatusUsuario
from models.material import Material, StatusMaterial
from models.space import Space, TipoEspaco
from models.event import Event, TipoEvento, StatusEvento
from models.achievement import Achievement, Collection


def add_mock_users(count=5):
    """Add mock producer users."""
    print(f"Adding {count} mock users...")

    first_names = ['Ana', 'Carlos', 'Beatriz', 'Diego', 'Elena', 'Fernando', 'Gabriela', 'Hugo', 'Isabel', 'Jorge']
    last_names = ['Oliveira', 'Santos', 'Pereira', 'Costa', 'Ferreira', 'Almeida', 'Souza', 'Lima', 'Gomes', 'Ribeiro']

    users_created = 0
    for i in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@email.com"

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            continue

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            tipo=TipoUsuario.PRODUCER.value,
            status=random.choice([StatusUsuario.ATIVO.value, StatusUsuario.PENDENTE.value]),
            pontos=random.randint(0, 500),
            is_active=True
        )
        user.set_password('senha123')
        db.session.add(user)
        users_created += 1

    db.session.commit()
    print(f"  Created {users_created} users")
    return users_created


def add_mock_materials(count=10):
    """Add mock materials from random producers."""
    print(f"Adding {count} mock materials...")

    producers = User.query.filter_by(tipo=TipoUsuario.PRODUCER.value, status=StatusUsuario.ATIVO.value).all()
    curators = User.query.filter_by(tipo=TipoUsuario.CURATOR.value).all()

    if not producers:
        print("  No active producers found!")
        return 0

    material_templates = [
        ('Garrafas PET', 'plastico', 'Garrafas plásticas limpas e sem rótulo'),
        ('Papelão', 'papel', 'Caixas de papelão desmontadas'),
        ('Latas de Alumínio', 'metal', 'Latas de refrigerante e cerveja'),
        ('Garrafas de Vidro', 'vidro', 'Garrafas de vidro limpas'),
        ('Jornais e Revistas', 'papel', 'Jornais e revistas antigos'),
        ('Embalagens Plásticas', 'plastico', 'Embalagens de produtos diversos'),
        ('Celulares Antigos', 'eletronicos', 'Celulares que não funcionam mais'),
        ('Pilhas e Baterias', 'eletronicos', 'Pilhas e baterias usadas'),
        ('Restos de Comida', 'organico', 'Restos orgânicos para compostagem'),
        ('Tampinhas Plásticas', 'plastico', 'Tampinhas de garrafas PET'),
        ('Latas de Conserva', 'metal', 'Latas de alimentos enlatados'),
        ('Potes de Vidro', 'vidro', 'Potes de conserva e geleias'),
    ]

    locations = [
        'Centro, próximo à praça',
        'Bairro Norte, Rua das Palmeiras',
        'Zona Sul, Av. Principal',
        'Condomínio Verde',
        'Empresa XYZ, sala 101',
        'Residência, Bairro Jardim',
        'Shopping Center',
        'Universidade Federal',
    ]

    quantities = ['5 unidades', '10 unidades', '20 unidades', '5kg', '10kg', '15kg', '1 sacola', '2 sacolas']

    feedbacks_approved = [
        'Material em excelente estado!',
        'Muito bem separado, parabéns!',
        'Qualidade excepcional.',
        'Material pronto para reciclagem.',
        '',
    ]

    feedbacks_rejected = [
        'Material contaminado, por favor limpar antes de enviar.',
        'Mistura de categorias não permitida.',
        'Por favor, forneça mais detalhes sobre o material.',
        'Material muito danificado para reciclagem.',
        'Quantidade insuficiente para coleta.',
    ]

    materials_created = 0
    for i in range(count):
        template = random.choice(material_templates)
        producer = random.choice(producers)
        status = random.choice([StatusMaterial.PENDING.value, StatusMaterial.APPROVED.value, StatusMaterial.REJECTED.value])

        material = Material(
            nome=template[0],
            categoria=template[1],
            descricao=template[2],
            localizacao=random.choice(locations),
            quantidade=random.choice(quantities),
            status=status,
            produtor_id=producer.id,
            criado_em=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )

        if status in [StatusMaterial.APPROVED.value, StatusMaterial.REJECTED.value] and curators:
            material.curador_id = random.choice(curators).id
            material.revisado_em = datetime.utcnow() - timedelta(days=random.randint(0, 7))

            if status == StatusMaterial.APPROVED.value:
                material.feedback = random.choice(feedbacks_approved)
                material.pontos_concedidos = random.randint(30, 100)
            else:
                material.feedback = random.choice(feedbacks_rejected)

        db.session.add(material)
        materials_created += 1

    db.session.commit()
    print(f"  Created {materials_created} materials")
    return materials_created


def add_mock_collections(count=10):
    """Add mock collection history for producers."""
    print(f"Adding {count} mock collections...")

    producers = User.query.filter_by(tipo=TipoUsuario.PRODUCER.value, status=StatusUsuario.ATIVO.value).all()

    if not producers:
        print("  No active producers found!")
        return 0

    material_names = [
        ('Garrafas PET', 'plastico'),
        ('Papelão', 'papel'),
        ('Latas de Alumínio', 'metal'),
        ('Vidros', 'vidro'),
        ('Eletrônicos', 'eletronicos'),
        ('Orgânicos', 'organico'),
    ]

    feedbacks = [
        'Excelente qualidade!',
        'Material bem separado.',
        'Ótima contribuição!',
        'Muito bom, continue assim!',
        'Perfeito estado para reciclagem.',
        '',
    ]

    quantities = ['10 unidades', '20 unidades', '50 unidades', '5kg', '10kg', '15kg', '25kg']

    collections_created = 0
    for i in range(count):
        producer = random.choice(producers)
        material = random.choice(material_names)

        collection = Collection(
            material_nome=material[0],
            categoria=material[1],
            quantidade=random.choice(quantities),
            pontos=random.randint(20, 200),
            feedback=random.choice(feedbacks),
            produtor_id=producer.id,
            data_coleta=datetime.utcnow() - timedelta(days=random.randint(1, 60))
        )

        db.session.add(collection)
        collections_created += 1

    db.session.commit()
    print(f"  Created {collections_created} collections")
    return collections_created


def add_mock_events(count=5):
    """Add mock future events."""
    print(f"Adding {count} mock events...")

    event_templates = [
        ('Coleta de Eletrônicos', TipoEvento.COLETA.value, 'Coleta especial de equipamentos eletrônicos'),
        ('Workshop de Reciclagem', TipoEvento.WORKSHOP.value, 'Aprenda técnicas de reciclagem doméstica'),
        ('Feira Verde', TipoEvento.EVENTO.value, 'Feira de produtos sustentáveis'),
        ('Curso de Compostagem', TipoEvento.CURSO.value, 'Curso prático de compostagem'),
        ('Mutirão de Limpeza', TipoEvento.EVENTO.value, 'Mutirão comunitário de limpeza'),
        ('Palestra Sustentabilidade', TipoEvento.EVENTO.value, 'Palestra sobre práticas sustentáveis'),
        ('Coleta de Óleo', TipoEvento.COLETA.value, 'Coleta de óleo de cozinha usado'),
        ('Workshop de Artesanato', TipoEvento.WORKSHOP.value, 'Transforme resíduos em arte'),
    ]

    locations = [
        'Centro Comunitário',
        'Praça Central',
        'Parque Municipal',
        'Escola Municipal',
        'Clube de Bairro',
        'Shopping Center',
    ]

    times = ['9:00 - 12:00', '14:00 - 17:00', '10:00 - 16:00', '8:00 - 18:00']

    events_created = 0
    for i in range(count):
        template = random.choice(event_templates)

        event = Event(
            titulo=template[0],
            tipo=template[1],
            descricao=template[2],
            status=StatusEvento.AGENDADO.value,
            data_inicio=datetime.now() + timedelta(days=random.randint(1, 60)),
            horario=random.choice(times),
            localizacao_custom=random.choice(locations)
        )

        db.session.add(event)
        events_created += 1

    db.session.commit()
    print(f"  Created {events_created} events")
    return events_created


def add_mock_spaces(count=3):
    """Add mock collection points/spaces."""
    print(f"Adding {count} mock spaces...")

    space_templates = [
        ('Ecoponto', TipoEspaco.COLETA.value, 'Ponto de coleta de recicláveis'),
        ('Centro de Reciclagem', TipoEspaco.COLETA.value, 'Centro completo de reciclagem'),
        ('Sala de Eventos', TipoEspaco.EVENTO.value, 'Espaço para eventos e palestras'),
        ('Centro de Treinamento', TipoEspaco.CURSO.value, 'Local para cursos e workshops'),
    ]

    neighborhoods = ['Centro', 'Norte', 'Sul', 'Leste', 'Oeste', 'Jardim', 'Vila Nova']
    streets = ['Rua das Flores', 'Av. Principal', 'Rua do Parque', 'Av. Brasil', 'Rua Verde']
    hours = ['Seg-Sex: 8h-18h', 'Seg-Sáb: 7h-19h', 'Todos os dias: 9h-17h', 'Seg-Sex: 9h-17h']

    spaces_created = 0
    for i in range(count):
        template = random.choice(space_templates)
        neighborhood = random.choice(neighborhoods)

        space = Space(
            nome=f"{template[0]} {neighborhood}",
            tipo=template[1],
            endereco=f"{random.choice(streets)}, {random.randint(100, 999)} - {neighborhood}",
            horario=random.choice(hours),
            descricao=template[2],
            ativo=True
        )

        db.session.add(space)
        spaces_created += 1

    db.session.commit()
    print(f"  Created {spaces_created} spaces")
    return spaces_created


def add_all_mock_data():
    """Add mock data to all tables."""
    app = create_app('development')

    with app.app_context():
        print("\n" + "=" * 50)
        print("ADDING MOCK DATA TO DATABASE")
        print("=" * 50 + "\n")

        users = add_mock_users(5)
        materials = add_mock_materials(15)
        collections = add_mock_collections(10)
        events = add_mock_events(5)
        spaces = add_mock_spaces(3)

        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"  Users created: {users}")
        print(f"  Materials created: {materials}")
        print(f"  Collections created: {collections}")
        print(f"  Events created: {events}")
        print(f"  Spaces created: {spaces}")
        print("\n[SUCCESS] Mock data added successfully!\n")


def show_menu():
    """Show interactive menu."""
    app = create_app('development')

    with app.app_context():
        while True:
            print("\n" + "=" * 50)
            print("MOCK DATA GENERATOR")
            print("=" * 50)
            print("1. Add mock users (5)")
            print("2. Add mock materials (15)")
            print("3. Add mock collections (10)")
            print("4. Add mock events (5)")
            print("5. Add mock spaces (3)")
            print("6. Add ALL mock data")
            print("7. Show current database stats")
            print("0. Exit")
            print("=" * 50)

            choice = input("Choose an option: ").strip()

            if choice == '1':
                add_mock_users(5)
            elif choice == '2':
                add_mock_materials(15)
            elif choice == '3':
                add_mock_collections(10)
            elif choice == '4':
                add_mock_events(5)
            elif choice == '5':
                add_mock_spaces(3)
            elif choice == '6':
                add_mock_users(5)
                add_mock_materials(15)
                add_mock_collections(10)
                add_mock_events(5)
                add_mock_spaces(3)
                print("\n[SUCCESS] All mock data added!")
            elif choice == '7':
                print("\n--- DATABASE STATS ---")
                print(f"  Users: {User.query.count()}")
                print(f"  Materials: {Material.query.count()}")
                print(f"  Collections: {Collection.query.count()}")
                print(f"  Events: {Event.query.count()}")
                print(f"  Spaces: {Space.query.count()}")
                print(f"  Achievements: {Achievement.query.count()}")
            elif choice == '0':
                print("Goodbye!")
                break
            else:
                print("Invalid option, try again.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        add_all_mock_data()
    else:
        show_menu()
