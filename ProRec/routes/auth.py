"""
Authentication routes - Migrated from Django LoginView/LogoutView.
Handles user login and logout with role-based redirection.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from models.user import User, StatusUsuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login view - handles both GET (display form) and POST (process login).
    Migrated from Django LoginView.
    """
    # If user is already authenticated, redirect to their dashboard
    if current_user.is_authenticated:
        return redirect_by_tipo(current_user.tipo)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Check if user status is active
            if user.status == StatusUsuario.ATIVO.value:
                # Log the user in
                login_user(user, remember=request.form.get('remember', False))

                # Update last activity
                from datetime import datetime
                from extensions import db
                user.ultima_atividade = datetime.utcnow()
                db.session.commit()

                # Redirect based on user tipo
                return redirect_by_tipo(user.tipo)
            else:
                flash('Sua conta está pendente de aprovação.', 'warning')
        else:
            flash('Email ou senha inválidos.', 'error')

    # GET request or failed login - show login form
    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    """
    Logout view - logs out the current user.
    Migrated from Django LogoutView.
    """
    logout_user()
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('auth.login'))


def redirect_by_tipo(tipo):
    """
    Redirect user based on their tipo.

    Args:
        tipo: User type (1=admin, 2=curator, 3=producer)

    Returns:
        Redirect to appropriate dashboard
    """
    if tipo == 1:
        return redirect(url_for('admin.dashboard'))
    elif tipo == 2:
        return redirect(url_for('curator.dashboard'))
    elif tipo == 3:
        return redirect(url_for('producer.dashboard'))

    # Fallback to login
    return redirect(url_for('auth.login'))
