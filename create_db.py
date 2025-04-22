from main import db, app

with app.app_context():
    db.drop_all()  # Remove todas as tabelas existentes
    


    db.create_all()
    print("Tabelas criadas com sucesso!")