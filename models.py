from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bd import obtener_conexion

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        conexion = obtener_conexion()
        user_data = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, username, password_hash FROM usuarios WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
        conexion.close()
        
        if user_data:
            return User(id=user_data[0], username=user_data[1], password_hash=user_data[2])
        return None

    @staticmethod
    def get_by_username(username):
        conexion = obtener_conexion()
        user_data = None
        with conexion.cursor() as cursor:
            cursor.execute("SELECT id, username, password_hash FROM usuarios WHERE username = %s", (username,))
            user_data = cursor.fetchone()
        conexion.close()
        
        if user_data:
            return User(id=user_data[0], username=user_data[1], password_hash=user_data[2])
        return None

    @staticmethod
    def create(username, password):
        conexion = obtener_conexion()
        password_hash = generate_password_hash(password)
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
        conexion.commit()
        conexion.close()