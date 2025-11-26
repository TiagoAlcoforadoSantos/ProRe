"""
Authentication decorators - Migrated from Django decorators.
Role-based access control decorators for Flask routes.
"""
from functools import wraps
from flask import redirect, url_for, flash, abort
from flask_login import current_user


def user_type_required(allowed_types):
    """
    Decorator to restrict access based on user type.

    Args:
        allowed_types: list of integers [1, 2, 3] representing user tipos

    Usage:
        @user_type_required([1, 2])  # Allow admin and curator
        def some_view():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if user is authenticated
            if not current_user.is_authenticated:
                flash('Por favor, faça login para acessar esta página.', 'info')
                return redirect(url_for('auth.login'))

            # Check if user tipo is in allowed types
            if current_user.tipo not in allowed_types:
                flash('Você não tem permissão para acessar esta página.', 'error')
                abort(403)  # Forbidden

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """
    Decorator for admin-only views (tipo=1).

    Usage:
        @admin_required
        def admin_dashboard():
            pass
    """
    return user_type_required([1])(f)


def curator_required(f):
    """
    Decorator for curator-only views (tipo=2).

    Usage:
        @curator_required
        def curator_dashboard():
            pass
    """
    return user_type_required([2])(f)


def producer_required(f):
    """
    Decorator for producer-only views (tipo=3).

    Usage:
        @producer_required
        def producer_dashboard():
            pass
    """
    return user_type_required([3])(f)


def active_user_required(f):
    """
    Decorator to ensure user status is 'ativo'.

    Usage:
        @active_user_required
        def some_view():
            pass
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if not current_user.is_authenticated:
            flash('Por favor, faça login para acessar esta página.', 'info')
            return redirect(url_for('auth.login'))

        # Check if user is active
        if not current_user.is_ativo():
            flash('Sua conta está inativa ou pendente de aprovação.', 'warning')
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)
    return decorated_function
