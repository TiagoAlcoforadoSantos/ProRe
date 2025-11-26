"""
Producer routes - Dashboard and material management for producers.
"""
from flask import Blueprint, render_template
from flask_login import login_required
from decorators.auth import producer_required, active_user_required

producer_bp = Blueprint('producer', __name__, url_prefix='/produtor')


@producer_bp.route('/')
@login_required
@active_user_required
@producer_required
def dashboard():
    """
    Producer dashboard with 3 tabs:
    - History (collections and achievements)
    - Publish (material publication and collection points)
    - Map (events and collection points map)
    """
    # TODO: Fetch actual data from database
    return render_template('producer/dashboard.html')
