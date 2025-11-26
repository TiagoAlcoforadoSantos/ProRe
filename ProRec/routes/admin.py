"""
Admin routes - System administration, spaces, and user management.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from decorators.auth import admin_required, active_user_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@active_user_required
@admin_required
def dashboard():
    """
    Admin dashboard with 3 tabs:
    - Spaces (physical space management)
    - Calendar (event scheduling)
    - Users (user approval and management)
    """
    # TODO: Fetch actual data from database
    return render_template('admin/dashboard.html')
