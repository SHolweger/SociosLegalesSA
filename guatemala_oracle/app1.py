from flask import Flask
from routes.main_routes import main_bp
from interface.interfaz_routes import interfaz_bp

app = Flask(__name__)
app.secret_key = "secreto_super"
app.register_blueprint(main_bp)
app.register_blueprint(interfaz_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')