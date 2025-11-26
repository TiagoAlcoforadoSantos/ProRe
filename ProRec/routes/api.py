"""
API routes - REST API endpoints for dashboard data.
"""
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from decorators.auth import producer_required, curator_required, admin_required, active_user_required
from models import (
    User, TipoUsuario, StatusUsuario,
    Material, StatusMaterial,
    Space, Event, StatusEvento,
    Achievement, Collection
)

api_bp = Blueprint('api', __name__, url_prefix='/api')


# =============================================================================
# Producer API Endpoints
# =============================================================================

@api_bp.route('/producer/stats')
@login_required
@active_user_required
@producer_required
def producer_stats():
    """Get producer statistics."""
    user_id = current_user.id

    # Count completed collections
    collections_count = Collection.query.filter_by(produtor_id=user_id).count()

    # Get achievements
    achievements = Achievement.query.order_by(Achievement.ordem).all()
    unlocked_count = sum(1 for a in achievements if current_user.pontos >= a.pontos_necessarios)
    total_achievements = len(achievements)

    return jsonify({
        'points': current_user.pontos,
        'collections_completed': collections_count,
        'achievements_unlocked': unlocked_count,
        'achievements_total': total_achievements
    })


@api_bp.route('/producer/achievements')
@login_required
@active_user_required
@producer_required
def producer_achievements():
    """Get producer achievements."""
    achievements = Achievement.query.order_by(Achievement.ordem).all()
    return jsonify([a.to_dict(current_user.pontos) for a in achievements])


@api_bp.route('/producer/collections')
@login_required
@active_user_required
@producer_required
def producer_collections():
    """Get producer collection history."""
    collections = Collection.query.filter_by(produtor_id=current_user.id)\
        .order_by(Collection.data_coleta.desc())\
        .limit(20).all()
    return jsonify([c.to_dict() for c in collections])


@api_bp.route('/producer/materials')
@login_required
@active_user_required
@producer_required
def producer_materials():
    """Get producer's published materials."""
    materials = Material.query.filter_by(produtor_id=current_user.id)\
        .order_by(Material.criado_em.desc())\
        .all()
    return jsonify([m.to_dict() for m in materials])


@api_bp.route('/producer/materials', methods=['POST'])
@login_required
@active_user_required
@producer_required
def producer_create_material():
    """Create a new material publication."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['name', 'category', 'description', 'location']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Field {field} is required'}), 400

    material = Material(
        nome=data['name'],
        categoria=data['category'],
        descricao=data['description'],
        localizacao=data['location'],
        quantidade=data.get('quantity'),
        produtor_id=current_user.id,
        status=StatusMaterial.PENDING.value
    )

    db.session.add(material)
    db.session.commit()

    return jsonify(material.to_dict()), 201


@api_bp.route('/producer/collection-points')
@login_required
@active_user_required
@producer_required
def producer_collection_points():
    """Get nearby collection points."""
    # Get all active collection spaces
    spaces = Space.query.filter_by(tipo='coleta', ativo=True).all()

    # Transform to expected format with distance placeholder
    collection_points = []
    for space in spaces:
        collection_points.append({
            'id': space.id,
            'name': space.nome,
            'address': space.endereco,
            'hours': space.horario or 'Horário não definido',
            'distance': 'N/A'  # Would need geolocation to calculate
        })

    return jsonify(collection_points)


@api_bp.route('/producer/events/today')
@login_required
@active_user_required
@producer_required
def producer_events_today():
    """Get events happening today."""
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    events = Event.query.filter(
        Event.data_inicio >= datetime.combine(today, datetime.min.time()),
        Event.data_inicio < datetime.combine(tomorrow, datetime.min.time()),
        Event.status.in_([StatusEvento.AGENDADO.value, StatusEvento.EM_ANDAMENTO.value])
    ).all()

    return jsonify([e.to_dict() for e in events])


# =============================================================================
# Curator API Endpoints
# =============================================================================

@api_bp.route('/curator/stats')
@login_required
@active_user_required
@curator_required
def curator_stats():
    """Get curator statistics."""
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())

    pending_count = Material.query.filter_by(status=StatusMaterial.PENDING.value).count()

    approved_today = Material.query.filter(
        Material.status == StatusMaterial.APPROVED.value,
        Material.revisado_em >= today_start,
        Material.revisado_em <= today_end,
        Material.curador_id == current_user.id
    ).count()

    rejected_today = Material.query.filter(
        Material.status == StatusMaterial.REJECTED.value,
        Material.revisado_em >= today_start,
        Material.revisado_em <= today_end,
        Material.curador_id == current_user.id
    ).count()

    return jsonify({
        'pending': pending_count,
        'approved_today': approved_today,
        'rejected_today': rejected_today
    })


@api_bp.route('/curator/pending-materials')
@login_required
@active_user_required
@curator_required
def curator_pending_materials():
    """Get pending materials for review."""
    materials = Material.query.filter_by(status=StatusMaterial.PENDING.value)\
        .order_by(Material.criado_em.desc())\
        .all()
    return jsonify([m.to_dict() for m in materials])


@api_bp.route('/curator/review-history')
@login_required
@active_user_required
@curator_required
def curator_review_history():
    """Get curator's review history."""
    materials = Material.query.filter(
        Material.curador_id == current_user.id,
        Material.status.in_([StatusMaterial.APPROVED.value, StatusMaterial.REJECTED.value])
    ).order_by(Material.revisado_em.desc()).limit(20).all()

    return jsonify([{
        'id': m.id,
        'name': m.nome,
        'status': m.status,
        'reviewDate': m.revisado_em.strftime('%d/%m/%Y') if m.revisado_em else None,
        'feedback': m.feedback or ''
    } for m in materials])


@api_bp.route('/curator/materials/<int:material_id>/approve', methods=['POST'])
@login_required
@active_user_required
@curator_required
def curator_approve_material(material_id):
    """Approve a material."""
    material = Material.query.get_or_404(material_id)

    if material.status != StatusMaterial.PENDING.value:
        return jsonify({'error': 'Material already reviewed'}), 400

    data = request.get_json() or {}
    feedback = data.get('feedback', '')
    points = data.get('points', 50)  # Default points for approval

    material.status = StatusMaterial.APPROVED.value
    material.curador_id = current_user.id
    material.revisado_em = datetime.utcnow()
    material.feedback = feedback
    material.pontos_concedidos = points

    # Award points to producer
    producer = material.produtor
    if producer:
        producer.pontos += points

        # Create collection record
        collection = Collection(
            material_nome=material.nome,
            categoria=material.categoria,
            quantidade=material.quantidade,
            pontos=points,
            feedback=feedback,
            produtor_id=producer.id,
            material_id=material.id
        )
        db.session.add(collection)

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Material "{material.nome}" aprovado com sucesso!',
        'material': material.to_dict()
    })


@api_bp.route('/curator/materials/<int:material_id>/reject', methods=['POST'])
@login_required
@active_user_required
@curator_required
def curator_reject_material(material_id):
    """Reject a material."""
    material = Material.query.get_or_404(material_id)

    if material.status != StatusMaterial.PENDING.value:
        return jsonify({'error': 'Material already reviewed'}), 400

    data = request.get_json() or {}
    feedback = data.get('feedback', '')

    if not feedback:
        return jsonify({'error': 'Feedback is required for rejection'}), 400

    material.status = StatusMaterial.REJECTED.value
    material.curador_id = current_user.id
    material.revisado_em = datetime.utcnow()
    material.feedback = feedback

    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Material "{material.nome}" reprovado.',
        'material': material.to_dict()
    })


# =============================================================================
# Admin API Endpoints
# =============================================================================

@api_bp.route('/admin/stats')
@login_required
@active_user_required
@admin_required
def admin_stats():
    """Get admin dashboard statistics."""
    total_spaces = Space.query.count()
    scheduled_events = Event.query.filter(
        Event.status.in_([StatusEvento.AGENDADO.value, StatusEvento.EM_ANDAMENTO.value])
    ).count()
    pending_users = User.query.filter_by(status=StatusUsuario.PENDENTE.value).count()
    total_users = User.query.count()
    active_users = User.query.filter_by(status=StatusUsuario.ATIVO.value).count()

    return jsonify({
        'total_spaces': total_spaces,
        'scheduled_events': scheduled_events,
        'pending_users': pending_users,
        'total_users': total_users,
        'active_users': active_users
    })


@api_bp.route('/admin/spaces')
@login_required
@active_user_required
@admin_required
def admin_spaces():
    """Get all spaces."""
    spaces = Space.query.order_by(Space.nome).all()
    return jsonify([s.to_dict() for s in spaces])


@api_bp.route('/admin/spaces', methods=['POST'])
@login_required
@active_user_required
@admin_required
def admin_create_space():
    """Create a new space."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['name', 'type', 'address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Field {field} is required'}), 400

    space = Space(
        nome=data['name'],
        tipo=data['type'],
        endereco=data['address'],
        horario=data.get('hours'),
        descricao=data.get('description')
    )

    db.session.add(space)
    db.session.commit()

    return jsonify(space.to_dict()), 201


@api_bp.route('/admin/spaces/<int:space_id>', methods=['PUT'])
@login_required
@active_user_required
@admin_required
def admin_update_space(space_id):
    """Update a space."""
    space = Space.query.get_or_404(space_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'name' in data:
        space.nome = data['name']
    if 'type' in data:
        space.tipo = data['type']
    if 'address' in data:
        space.endereco = data['address']
    if 'hours' in data:
        space.horario = data['hours']
    if 'description' in data:
        space.descricao = data['description']
    if 'active' in data:
        space.ativo = data['active']

    db.session.commit()

    return jsonify(space.to_dict())


@api_bp.route('/admin/events')
@login_required
@active_user_required
@admin_required
def admin_events():
    """Get upcoming events."""
    events = Event.query.filter(
        Event.data_inicio >= datetime.now()
    ).order_by(Event.data_inicio).limit(20).all()

    return jsonify([e.to_dict() for e in events])


@api_bp.route('/admin/events', methods=['POST'])
@login_required
@active_user_required
@admin_required
def admin_create_event():
    """Create a new event."""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    required_fields = ['title', 'type', 'date']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Field {field} is required'}), 400

    event = Event(
        titulo=data['title'],
        tipo=data['type'],
        descricao=data.get('description'),
        data_inicio=datetime.fromisoformat(data['date']),
        horario=data.get('time'),
        espaco_id=data.get('space_id'),
        localizacao_custom=data.get('location')
    )

    db.session.add(event)
    db.session.commit()

    return jsonify(event.to_dict()), 201


@api_bp.route('/admin/pending-users')
@login_required
@active_user_required
@admin_required
def admin_pending_users():
    """Get pending users for approval."""
    users = User.query.filter_by(status=StatusUsuario.PENDENTE.value).all()

    result = []
    for user in users:
        name = user.get_full_name()
        initials = ''.join([n[0].upper() for n in name.split()[:2]]) if name else 'U'
        result.append({
            'id': user.id,
            'name': name,
            'email': user.email,
            'initials': initials
        })

    return jsonify(result)


@api_bp.route('/admin/active-users')
@login_required
@active_user_required
@admin_required
def admin_active_users():
    """Get active users."""
    users = User.query.filter_by(status=StatusUsuario.ATIVO.value)\
        .order_by(User.ultima_atividade.desc())\
        .limit(50).all()

    type_display_map = {
        TipoUsuario.ADMIN.value: 'Administrador',
        TipoUsuario.CURATOR.value: 'Curador',
        TipoUsuario.PRODUCER.value: 'Produtor'
    }
    type_key_map = {
        TipoUsuario.ADMIN.value: 'admin',
        TipoUsuario.CURATOR.value: 'curator',
        TipoUsuario.PRODUCER.value: 'producer'
    }

    result = []
    for user in users:
        name = user.get_full_name()
        initials = ''.join([n[0].upper() for n in name.split()[:2]]) if name else 'U'

        # Calculate last activity text
        if user.ultima_atividade:
            diff = datetime.utcnow() - user.ultima_atividade
            if diff.days > 0:
                last_activity = f'{diff.days} dias atrás'
            elif diff.seconds >= 3600:
                hours = diff.seconds // 3600
                last_activity = f'{hours} hora{"s" if hours > 1 else ""} atrás'
            elif diff.seconds >= 60:
                minutes = diff.seconds // 60
                last_activity = f'{minutes} min atrás'
            else:
                last_activity = 'Agora mesmo'
        else:
            last_activity = 'Nunca'

        result.append({
            'id': user.id,
            'name': name,
            'email': user.email,
            'type': type_key_map.get(user.tipo, 'producer'),
            'type_display': type_display_map.get(user.tipo, 'Produtor'),
            'initials': initials,
            'last_activity': last_activity
        })

    return jsonify(result)


@api_bp.route('/admin/users/<int:user_id>/approve', methods=['POST'])
@login_required
@active_user_required
@admin_required
def admin_approve_user(user_id):
    """Approve a pending user."""
    user = User.query.get_or_404(user_id)

    if user.status != StatusUsuario.PENDENTE.value:
        return jsonify({'error': 'User is not pending'}), 400

    user.status = StatusUsuario.ATIVO.value
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Usuário {user.get_full_name()} aprovado com sucesso!'
    })


@api_bp.route('/admin/users/<int:user_id>/reject', methods=['POST'])
@login_required
@active_user_required
@admin_required
def admin_reject_user(user_id):
    """Reject a pending user."""
    user = User.query.get_or_404(user_id)

    if user.status != StatusUsuario.PENDENTE.value:
        return jsonify({'error': 'User is not pending'}), 400

    user.status = StatusUsuario.INATIVO.value
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Usuário {user.get_full_name()} rejeitado.'
    })


@api_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@login_required
@active_user_required
@admin_required
def admin_update_user(user_id):
    """Update user information."""
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        user.email = data['email']
    if 'tipo' in data:
        user.tipo = data['tipo']
    if 'status' in data:
        user.status = data['status']

    db.session.commit()

    return jsonify(user.to_dict())
