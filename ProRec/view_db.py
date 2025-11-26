"""Quick script to view database contents."""
from app import create_app
from extensions import db
from models import User, Material, Space, Event, Achievement, Collection

def view_database():
    app = create_app('development')

    with app.app_context():
        print("=" * 60)
        print("USERS")
        print("=" * 60)
        for user in User.query.all():
            print(f"  [{user.id}] {user.get_full_name()} ({user.email})")
            print(f"      Type: {user.get_tipo_display()}, Status: {user.status}, Points: {user.pontos}")

        print("\n" + "=" * 60)
        print("MATERIALS")
        print("=" * 60)
        for m in Material.query.all():
            print(f"  [{m.id}] {m.nome} - {m.get_categoria_display()}")
            print(f"      Status: {m.status}, Producer ID: {m.produtor_id}")

        print("\n" + "=" * 60)
        print("SPACES")
        print("=" * 60)
        for s in Space.query.all():
            print(f"  [{s.id}] {s.nome} ({s.get_tipo_display()})")
            print(f"      Address: {s.endereco}")

        print("\n" + "=" * 60)
        print("EVENTS")
        print("=" * 60)
        for e in Event.query.all():
            print(f"  [{e.id}] {e.titulo} ({e.get_tipo_display()})")
            print(f"      Date: {e.data_inicio}, Location: {e.get_localizacao()}")

        print("\n" + "=" * 60)
        print("ACHIEVEMENTS")
        print("=" * 60)
        for a in Achievement.query.all():
            print(f"  [{a.id}] {a.icone} {a.nome} - {a.pontos_necessarios} pts required")

        print("\n" + "=" * 60)
        print("COLLECTIONS (History)")
        print("=" * 60)
        for c in Collection.query.all():
            print(f"  [{c.id}] {c.material_nome} - {c.pontos} pts")
            print(f"      Date: {c.data_coleta}")

if __name__ == '__main__':
    view_database()
