from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('juegos'))
        flash('Usuario o contraseña inválidos', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_by_username(form.username.data):
            flash('El nombre de usuario ya existe', 'danger')
        else:
            User.create(form.username.data, form.password.data)
            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)