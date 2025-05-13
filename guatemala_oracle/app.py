from flask import Flask
from routes import main_routes
from config.config import get_db_connection, Base

app = Flask(__name__)

engine, SessionLocal, _ = get_db_connection()

if engine:
    Base.metadata.create_all(bind=engine)
    app.register_blueprint(main_routes.main_bp)
    app.config["SESSION_LOCAL"] = SessionLocal  
else:
    print("No se pudo conectar a la base de datos. Verifica tu archivo .env.")


if __name__ == "__main__":
    app.run(debug=False, port=5001, host="0.0.0.0") 