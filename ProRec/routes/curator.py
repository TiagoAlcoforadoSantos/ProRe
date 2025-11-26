"""
Curator routes - Material review and approval for curators.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from decorators.auth import curator_required, active_user_required

curator_bp = Blueprint('curator', __name__, url_prefix='/curador')


@curator_bp.route('/')
@login_required
@active_user_required
@curator_required
def dashboard():
    """
    Curator dashboard with:
    - Stats cards (pending, approved today, rejected today)
    - Pending materials review queue
    - Approve/reject actions
    """
    # TODO: Fetch actual data from database
    return render_template('curator/dashboard.html')
