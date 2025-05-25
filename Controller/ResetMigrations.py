from ..Models import db

def reset_migrations(app):
    with app.app_context():
        print("🔄 Resetando o banco de dados...")
        db.drop_all()
        db.create_all()
        print("✅ Banco resetado.")