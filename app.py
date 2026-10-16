from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required
import controlador_juegos
from models import User
from auth import auth_bp

app = Flask(__name__)
# Clave secreta requerida por WTForms y las sesiones
app.config['SECRET_KEY'] = 'mi_llave_super_secreta_123'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # Redirige aquí si no está logueado
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Registro del blueprint de autenticación
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/agregar_juego")
@login_required
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.insertar_juego(nombre, descripcion, precio)
    return redirect("/juegos")

@app.route("/")
@app.route("/juegos")
@login_required
def juegos():
    juegos = controlador_juegos.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/eliminar_juego", methods=["POST"])
@login_required
def eliminar_juego():
    controlador_juegos.eliminar_juego(request.form["id"])
    return redirect("/juegos")

@app.route("/formulario_editar_juego/<int:id>")
@login_required
def editar_juego(id):
    juego = controlador_juegos.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controlador_juegos.actualizar_juego(nombre, descripcion, precio, id)
    return redirect("/juegos")

if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)