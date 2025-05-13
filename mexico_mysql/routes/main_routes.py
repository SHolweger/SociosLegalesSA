from flask import Blueprint, request, current_app, jsonify
from services.cliente_service import get_clientes, create_cliente, update_cliente, delete_cliente, get_cliente_by_id
from services.asunto_service import get_asuntos, create_asunto, update_asunto, delete_asunto, get_asunto_by_id
from services.procurador_service import get_procuradores, create_procurador, update_procurador, delete_procurador, get_procurador_by_id
from services.abogado_service import get_abogados, create_abogado, update_abogado, delete_abogado, get_abogado_by_dni
from services.audiencia_service import get_audiencias, create_audiencia, update_audiencia, delete_audiencia, get_audiencia_by_id
from services.incidencias_service import get_incidencias, create_incidencia, update_incidencia, delete_incidencia, get_incidencia_by_id
from services.asunto_procurador_service import get_asunto_procuradores, assign_procurador_to_asunto
import os
import pymysql

main_bp = Blueprint("main", __name__)

@main_bp.route('/check_db', methods=['GET'])
def check_db():
    try:
        db_host = os.getenv("DB_HOST")
        db_port = int(os.getenv("DB_PORT", "3306"))
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")

        connection = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            connect_timeout=5
        )

        if connection.open:
            return jsonify({"message": "Conexión exitosa a Sucursal MySQL México"}), 200
    except pymysql.MySQLError as e:
        return jsonify({"error": f"Error al conectar a Sucursal MySQL México: {str(e)}"}), 500
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()

# ---- CLIENTES ----
@main_bp.route("/clientes", methods=["GET"]) #select
def route_get_clientes():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_clientes(SessionLocal)

@main_bp.route("/create/cliente", methods=["POST"]) #insert
def route_create_cliente():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_cliente(request.json, SessionLocal) 

@main_bp.route("/update/cliente/<int:id>", methods=["PUT"]) #update
def route_update_cliente(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_cliente(id, request.json, SessionLocal)

@main_bp.route(("/delete/cliente/<int:id>"), methods=["DELETE"]) #delete
def route_delete_cliente(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_cliente(id, SessionLocal)

@main_bp.route("/get/cliente/<int:id>", methods=["GET"]) #get by id
def route_get_cliente(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_cliente_by_id(id, SessionLocal)

# ---- ASUNTOS ----
@main_bp.route("/asuntos", methods=["GET"]) #select
def route_get_asuntos():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_asuntos(SessionLocal)

@main_bp.route("/create/asunto", methods=["POST"]) #insert
def route_create_asunto():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_asunto(request.json, SessionLocal)

@main_bp.route("/update/asunto/<int:id>", methods=["PUT"]) #update
def route_update_asunto(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_asunto(id, request.json, SessionLocal)

@main_bp.route(("/delete/asunto/<int:id>"), methods=["DELETE"]) #delete
def route_delete_asunto(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_asunto(id, SessionLocal)

@main_bp.route("/get/asunto/<int:id>", methods=["GET"]) #get by id
def route_get_asunto(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_asunto_by_id(id, SessionLocal)

# ---- PROCURADORES ----
@main_bp.route("/procuradores", methods=["GET"])
def route_get_procuradores():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_procuradores(SessionLocal)

@main_bp.route("/create/procurador", methods=["POST"])
def route_create_procurador():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_procurador(request.json, SessionLocal)

@main_bp.route("/update/procurador/<int:id>", methods=["PUT"])
def route_update_procurador(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_procurador(id, request.json, SessionLocal)

@main_bp.route("/delete/procurador/<int:id>", methods=["DELETE"])
def route_delete_procurador(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_procurador(id, SessionLocal)

@main_bp.route("/get/procurador/<int:id>", methods=["GET"])
def route_get_procurador(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_procurador_by_id(id, SessionLocal)

# ---- ABOGADOS ----
@main_bp.route("/abogados", methods=["GET"])
def route_get_abogados():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_abogados(SessionLocal)

@main_bp.route("/create/abogado", methods=["POST"])
def route_create_abogado():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_abogado(request.json, SessionLocal)

@main_bp.route("/update/abogado/<string:dni>", methods=["PUT"])
def route_update_abogado(dni):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_abogado(dni, request.json, SessionLocal)

@main_bp.route("/delete/abogado/<string:dni>", methods=["DELETE"])
def route_delete_abogado(dni):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_abogado(dni, SessionLocal)

@main_bp.route("/get/abogado/<string:dni>", methods=["GET"])
def route_get_abogado(dni):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_abogado_by_dni(dni, SessionLocal)

# ---- AUDIENCIAS ----
@main_bp.route("/audiencias", methods=["GET"])
def route_get_audiencias():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_audiencias(SessionLocal)

@main_bp.route("/create/audiencia", methods=["POST"])
def route_create_audiencia():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_audiencia(request.json, SessionLocal)

@main_bp.route("/update/audiencia/<int:id>", methods=["PUT"])
def route_update_audiencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_audiencia(id, request.json, SessionLocal)

@main_bp.route("/delete/audiencia/<int:id>", methods=["DELETE"])
def route_delete_audiencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_audiencia(id, SessionLocal)

@main_bp.route("/get/audiencia/<int:id>", methods=["GET"])
def route_get_audiencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_audiencia_by_id(id, SessionLocal)

# ---- INCIDENCIAS ----
@main_bp.route("/incidencias", methods=["GET"])
def route_get_incidencias():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_incidencias(SessionLocal)

@main_bp.route("/create/incidencia", methods=["POST"])
def route_create_incidencia():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return create_incidencia(request.json, SessionLocal)

@main_bp.route("/update/incidencia/<int:id>", methods=["PUT"])
def route_update_incidencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return update_incidencia(id, request.json, SessionLocal)

@main_bp.route("/delete/incidencia/<int:id>", methods=["DELETE"])
def route_delete_incidencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return delete_incidencia(id, SessionLocal)

@main_bp.route("/get/incidencia/<int:id>", methods=["GET"])
def route_get_incidencia(id):
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_incidencia_by_id(id, SessionLocal)

# ---- ASUNTO PROCURADOR (Relación M:N) ----
@main_bp.route("/asunto_procuradores", methods=["GET"])
def route_get_asunto_procuradores():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return get_asunto_procuradores(SessionLocal)

@main_bp.route("/assign/procurador", methods=["POST"])
def route_assign_procurador():
    SessionLocal = current_app.config["SESSION_LOCAL"]
    return assign_procurador_to_asunto(request.json, SessionLocal)