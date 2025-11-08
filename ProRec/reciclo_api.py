from flask import Flask, request, jsonify
from functools import wraps
from datetime import datetime
import jwt
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-super-segura'

# =====================================================
# FUNÇÕES AUXILIARES E DECORATORS
# =====================================================

def get_db_connection():
    """Estabelece conexão com o banco de dados SQLite"""
    conn = sqlite3.connect('reciclo.db')
    conn.row_factory = sqlite3.Row
    return conn

def token_required(f):
    """Decorator para proteger rotas que precisam de autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'mensagem': 'Token não fornecido'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data
        except:
            return jsonify({'mensagem': 'Token inválido'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

def funcionario_required(f):
    """Decorator para rotas que só funcionários podem acessar"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user['perfil'] != 'funcionario':
            return jsonify({'mensagem': 'Acesso negado. Apenas funcionários podem acessar'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated

# =====================================================
# ROTAS DE AUTENTICAÇÃO
# =====================================================

@app.route('/api/login', methods=['POST'])
def login():
    """
    Rota de login - retorna token JWT
    Exemplo de requisição:
    {
        "email": "admin_re@re.com",
        "senha": "admin123"
    }
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    conn = get_db_connection()
    usuario = conn.execute(
        'SELECT * FROM usuarios WHERE email = ?',
        (data['email'],)
    ).fetchone()
    conn.close()
    
    if not usuario or not check_password_hash(usuario['senha'], data['senha']):
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401
    
    token = jwt.encode({
        'id': usuario['id'],
        'email': usuario['email'],
        'perfil': usuario['perfil'],
        'nome': usuario['nome']
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'token': token,
        'usuario': {
            'id': usuario['id'],
            'nome': usuario['nome'],
            'email': usuario['email'],
            'perfil': usuario['perfil']
        }
    }), 200

# =====================================================
# ROTAS DE USUÁRIOS
# =====================================================

@app.route('/api/usuarios', methods=['POST'])
@funcionario_required
def cadastrar_usuario(current_user):
    """
    Cadastra um novo usuário (apenas funcionários)
    Exemplo de requisição:
    {
        "nome": "João Silva",
        "email": "joao@email.com",
        "senha": "senha123",
        "perfil": "cliente",
        "telefone": "81999999999"
    }
    """
    data = request.get_json()
    
    # Validações
    if not data or not all(k in data for k in ('nome', 'email', 'senha', 'perfil')):
        return jsonify({'mensagem': 'Dados incompletos'}), 400
    
    if data['perfil'] not in ['funcionario', 'cliente']:
        return jsonify({'mensagem': 'Perfil inválido. Use "funcionario" ou "cliente"'}), 400
    
    conn = get_db_connection()
    
    # Verifica se o email já existe
    usuario_existe = conn.execute(
        'SELECT id FROM usuarios WHERE email = ?',
        (data['email'],)
    ).fetchone()
    
    if usuario_existe:
        conn.close()
        return jsonify({'mensagem': 'Email já cadastrado'}), 409
    
    # Insere novo usuário
    senha_hash = generate_password_hash(data['senha'])
    cursor = conn.execute(
        'INSERT INTO usuarios (nome, email, senha, perfil, telefone) VALUES (?, ?, ?, ?, ?)',
        (data['nome'], data['email'], senha_hash, data['perfil'], data.get('telefone', ''))
    )
    conn.commit()
    usuario_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'mensagem': 'Usuário cadastrado com sucesso',
        'usuario': {
            'id': usuario_id,
            'nome': data['nome'],
            'email': data['email'],
            'perfil': data['perfil']
        }
    }), 201

@app.route('/api/usuarios', methods=['GET'])
@funcionario_required
def listar_usuarios(current_user):
    """Lista todos os usuários (apenas funcionários)"""
    conn = get_db_connection()
    usuarios = conn.execute('SELECT id, nome, email, perfil, telefone, data_cadastro FROM usuarios').fetchall()
    conn.close()
    
    usuarios_lista = []
    for usuario in usuarios:
        usuarios_lista.append({
            'id': usuario['id'],
            'nome': usuario['nome'],
            'email': usuario['email'],
            'perfil': usuario['perfil'],
            'telefone': usuario['telefone'],
            'data_cadastro': usuario['data_cadastro']
        })
    
    return jsonify({'usuarios': usuarios_lista}), 200

@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
@token_required
def obter_usuario(current_user, usuario_id):
    """Obtém dados de um usuário específico"""
    # Clientes só podem ver seus próprios dados
    if current_user['perfil'] == 'cliente' and current_user['id'] != usuario_id:
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    conn = get_db_connection()
    usuario = conn.execute(
        'SELECT id, nome, email, perfil, telefone, data_cadastro FROM usuarios WHERE id = ?',
        (usuario_id,)
    ).fetchone()
    conn.close()
    
    if not usuario:
        return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'id': usuario['id'],
        'nome': usuario['nome'],
        'email': usuario['email'],
        'perfil': usuario['perfil'],
        'telefone': usuario['telefone'],
        'data_cadastro': usuario['data_cadastro']
    }), 200

# =====================================================
# ROTAS DE MATERIAIS
# =====================================================

@app.route('/api/residuos', methods=['POST'])
@funcionario_required
def cadastrar_residuo(current_user):
    """
    Cadastra um novo residuo(apenas funcionários)
    Exemplo de requisição:
    {
        "categoria": "Aluminio",
        "nome_residuo":"latas",
        "descricao":"latas de refrigerante",
        "quantidade_total": "20"
        "quantidade_disponivel": "90"
    }
    """
    data = request.get_json()
    
    # Validações
    if not data or not all(k in data for k in ('categoria','nome_residuo', 'descricao', 'quantidade_total')):
        return jsonify({'mensagem': 'Dados incompletos (categoria, nome_residuo, descricao e quantidade_total são obrigatórios)'}), 400
    
    conn = get_db_connection()
    
    # Verifica se o material já existe 
    if data.get('nome_residuo'):
        residuo_existe = conn.execute(
            'SELECT id FROM residuos WHERE nome_residuo = ?',
            (data['nome_residuo'],)
        ).fetchone()
        
        if residuo_existe:
            conn.close()
            return jsonify({'mensagem': 'nome_residuo já cadastrado'}), 409
    
    # Insere novo material
    cursor = conn.execute(
        '''INSERT INTO residuos 
           (categoria, nome_residuo, descricao, quantidade_total, quantidade_disponivel) 
           VALUES (?, ?, ?, ?, ?)''',
        (
            data.get('categoria', ''),
            data.get('nome_residuo'),
            data.get('descricao', ''),
            data['quantidade_total'],
            data['quantidade_disponivel']
        )
    )
    conn.commit()
    residuos_id = cursor.lastrowid
    conn.close()
    
    return jsonify({
        'mensagem': 'Material cadastrado com sucesso',
        'Material': {
            'id': residuos_id,
            'categoria': data['categoria'],
            'nome_residuo': data['nome_residuo'],
            'descricao': data.get('descricao', ''),
            'quantidade_total': data['quantidade_total']
        }
    }), 201

@app.route('/api/residuos', methods=['GET'])
def listar_residuo():

    categoria = request.args.get('categoria', '')
    nome_residuo = request.args.get('nome_residuo', '')
    descricao = request.args.get('descricao', '')
    disponivel = request.args.get('disponivel', '')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM residuos WHERE 1=1'
    params = []
    
    if categoria:
        query += ' AND categoria LIKE ?'
        params.append(f'%{categoria}%')
    
    if nome_residuo:
        query += ' AND nome_residuo LIKE ?'
        params.append(f'%{nome_residuo}%')
    
    if descricao:
        query += ' AND descricao LIKE ?'
        params.append(f'%{descricao}%')
    
    if disponivel.lower() == 'true':
        query += ' AND quantidade_disponivel > 0'
    
    residuos = conn.execute(query, params).fetchall()
    conn.close()
    
    residuos_lista = []
    for residuo in residuos:
        residuos_lista.append({
            'id': residuo['id'],
            'categoria': residuo['categoria'],
            'nome_residuo': residuo['nome_residuo'],
            'descricao': residuo['descricao'],
            'quantidade_total': residuo['quantidade_total'],
            'quantidade_disponivel': residuo['quantidade_disponivel']
        })
    
    return jsonify({'residuos': residuos_lista}), 200

@app.route('/api/residuos/<int:residuos_id>', methods=['GET'])
def obter_residuo(residuos_id):
    """Obtém dados de um material(rota pública)"""
    conn = get_db_connection()
    residuo = conn.execute('SELECT * FROM residuos WHERE id = ?', (residuos_id,)).fetchone()
    conn.close()
    
    if not residuo:
        return jsonify({'mensagem': 'material não encontrado'}), 404
    
    return jsonify({
        'id': residuo['id'],
        'categoria': residuo['categoria'],
        'nome_residuo': residuo['nome_residuo'],
        'descricao': residuo['descricao'],
        'quantidade_total': residuo['quantidade_total'],
        'quantidade_disponivel': residuo['quantidade_disponivel']
    }), 200

@app.route('/api/residuos/<int:residuos_id>', methods=['PUT'])
@funcionario_required
def atualizar_residuo(current_user, residuos_id):
    """Atualiza dados de um material (apenas funcionários)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'mensagem': 'Dados não fornecidos'}), 400
    
    conn = get_db_connection()
    
    # Verifica se o material existe
    residuos = conn.execute('SELECT * FROM residuos WHERE id = ?', (residuos_id,)).fetchone()
    if not residuos:
        conn.close()
        return jsonify({'mensagem': 'material não encontrado'}), 404
    
    # Atualiza apenas os campos fornecidos
    campos_atualizaveis = ['categoria','nome_residuo','descricao','quantidade_total']
    updates = []
    params = []
    
    for campo in campos_atualizaveis:
        if campo in data:
            updates.append(f'{campo} = ?')
            params.append(data[campo])
    
    # Atualiza quantidade_disponivel se a quantidade foi alterada
    if 'quantidade_total' in data:
        diferenca = data['quantidade_total'] - residuos['quantidade_total']
        nova_disponivel = residuos['quantidade_disponivel'] + diferenca
        updates.append('quantidade_disponivel = ?')
        params.append(max(0, nova_disponivel))
    
    if updates:
        params.append(residuos_id)
        query = f"UPDATE residuos SET {', '.join(updates)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()
    
    conn.close()
    
    return jsonify({'mensagem': 'material atualizado com sucesso'}), 200

@app.route('/api/residuos/<int:residuos_id>', methods=['DELETE'])
@funcionario_required
def deletar_residuo(current_user, residuos_id):
    """Deleta um material (apenas funcionários)"""
    conn = get_db_connection()
    
    # Verifica se existem reservas ativas para este material
    reservas_ativas = conn.execute(
        'SELECT COUNT(*) as total FROM reservas_residuo WHERE residuos_id = ? AND status = "ativa"',
        (residuos_id,)
    ).fetchone()
    
    if reservas_ativas['total'] > 0:
        conn.close()
        return jsonify({'mensagem': 'Não é possível deletar residuo com reservas ativas'}), 400
    
    cursor = conn.execute('DELETE FROM residuos WHERE id = ?', (residuos_id,))
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'mensagem': 'material não encontrado'}), 404
    
    conn.close()
    return jsonify({'mensagem': 'material deletado com sucesso'}), 200

# =====================================================
# ROTAS DE RESERVAS DE MATERIAIS
# =====================================================

@app.route('/api/reservas_residuo', methods=['POST'])
@token_required
def criar_reserva(current_user):
    """
    Cria uma nova reserva
    Exemplo de requisição:
    {
        "residuo_id": 1
    }
    """
    data = request.get_json()
    
    if not data or 'residuo_id' not in data:
        return jsonify({'mensagem': 'residuo_id é obrigatório'}), 400
    
    residuos_id = data['residuo_id']
    usuario_id = current_user['id']
    
    conn = get_db_connection()
    
    # Verifica se o material existe e está disponível
    residuo = conn.execute('SELECT * FROM residuos WHERE id = ?', (residuos_id,)).fetchone()
    
    if not residuo:
        conn.close()
        return jsonify({'mensagem': 'material não encontrado'}), 404
    
    if residuo['quantidade_disponivel'] <= 0:
        conn.close()
        return jsonify({'mensagem': 'material indisponível no momento'}), 400
    
    # Verifica se o usuário já tem reserva ativa deste material
    reserva_existente = conn.execute(
        'SELECT id FROM reservas_residuo WHERE usuario_id = ? AND residuos_id = ? AND status = "ativa"',
        (usuario_id, residuos_id)
    ).fetchone()
    
    if reserva_existente:
        conn.close()
        return jsonify({'mensagem': 'Você já possui uma reserva ativa deste material'}), 400

    # Cria a reserva
    data_retirada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = conn.execute(
        'INSERT INTO reservas_residuo (usuario_id, residuos_id, data_retirada, status) VALUES (?, ?, ?, ?)',
        (usuario_id, residuos_id, data_retirada, 'ativa')
    )
    reserva_id = cursor.lastrowid
    
    # Atualiza quantidade disponível de materiais
    conn.execute(
        'UPDATE residuos SET quantidade_disponivel = quantidade_disponivel - 1 WHERE id = ?',
        (residuos_id,)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'mensagem': 'Reserva criada com sucesso',
        'reserva': {
            'id': reserva_id,
            'residuos_id': residuos_id,
            'data_retirada': data_retirada,
            'status': 'ativa'
        }
    }), 201

@app.route('/api/reservas_residuo', methods=['GET'])
@token_required
def listar_reservas(current_user):
    """
    Lista reservas
    - Clientes veem apenas suas próprias reservas
    - Funcionários veem todas as reservas
    """
    conn = get_db_connection()
    
    if current_user['perfil'] == 'funcionario':
        # Funcionários veem todas as reservas
        reservas = conn.execute('''
            SELECT r.*, u.nome as usuario_nome, u.email as usuario_email,
                   l.categoria as categoria_titulo, l.nome_residuo as residuo_autor
            FROM reservas_residuo r
            JOIN usuarios u ON r.usuario_id = u.id
            JOIN residuos l ON r.residuos_id = l.id
            ORDER BY data_retirada DESC
        ''').fetchall()
    else:
        # Clientes veem apenas suas reservas
        reservas = conn.execute('''
            SELECT r.*, u.nome as usuario_nome, l.categoria as categoria_titulo
            FROM reservas_residuo r
            JOIN usuarios u ON r.usuario_id = u.id
            JOIN residuos l ON r.residuos_id = l.id;
            ORDER BY r.data_retirada DESC
        ''', (current_user['id'],)).fetchall()
    
    conn.close()
    
    reservas_lista = []
    for reserva in reservas:
        item = {
            'id': reserva['id'],
            'residuos_id': reserva['residuos_id'],
            'data_retirada': reserva['data_retirada'],
            'data_devolucao': reserva['data_devolucao'],
            'status': reserva['status']
        }
        
        # Adiciona informações do usuário apenas para funcionários
        if current_user['perfil'] == 'funcionario':
            item['usuario_id'] = reserva['usuario_id']
            item['usuario_nome'] = reserva['usuario_nome']
            item['usuario_email'] = reserva['usuario_email']
        
        reservas_lista.append(item)
    
    return jsonify({'reservas_residuo': reservas_lista}), 200

@app.route('/api/reservas_residuo/<int:reserva_id>/devolver', methods=['PUT'])
@token_required
def devolver_material(current_user, reserva_id):
    """Marca uma reserva como devolvida"""
    conn = get_db_connection()
    
    # Busca a reserva
    reserva = conn.execute('SELECT * FROM reservas_residuo WHERE id = ?', (reserva_id,)).fetchone()
    
    if not reserva:
        conn.close()
        return jsonify({'mensagem': 'Reserva não encontrada'}), 404
    
    # Verifica permissões: cliente só pode devolver suas próprias reservas
    if current_user['perfil'] == 'cliente' and reserva['usuario_id'] != current_user['id']:
        conn.close()
        return jsonify({'mensagem': 'Acesso negado'}), 403
    
    if reserva['status'] == 'devolvida':
        conn.close()
        return jsonify({'mensagem': 'material já foi devolvido'}), 400
    
    # Atualiza a reserva
    data_devolucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute(
        'UPDATE reservas_residuo SET status = ?, data_devolucao = ? WHERE id = ?',
        ('devolvida', data_devolucao, reserva_id)
    )
    
    # Atualiza quantidade disponível do material
    conn.execute(
        'UPDATE residuo SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id = ?',
        (reserva['residuos_id'],)
    )
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'mensagem': 'material devolvido com sucesso',
        'data_devolucao': data_devolucao
    }), 200

@app.route('/api/reservas_residuo/<int:reserva_id>', methods=['DELETE'])
@funcionario_required
def cancelar_reserva(current_user, reserva_id):
    """Cancela/deleta uma reserva (apenas funcionários)"""
    conn = get_db_connection()
    
    reserva = conn.execute('SELECT * FROM reservas_residuo WHERE id = ?', (reserva_id,)).fetchone()
    
    if not reserva:
        conn.close()
        return jsonify({'mensagem': 'Reserva não encontrada'}), 404
    
    # Se a reserva está ativa, devolve o material ao estoque
    if reserva['status'] == 'ativa':
        conn.execute(
            'UPDATE residuos SET quantidade_disponivel = quantidade_disponivel + 1 WHERE id = ?',
            (reserva['residuos_id'],)
        )
    
    conn.execute('DELETE FROM reservas_residuo WHERE id = ?', (reserva_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'mensagem': 'Reserva cancelada com sucesso'}), 200



# =====================================================
# ROTA DE STATUS DA API
# =====================================================

@app.route('/api/status', methods=['GET'])
def status():
    """Verifica se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'mensagem': 'API do reciclo funcionando',
        'versao': '1.0'
    }), 200

# =====================================================
# INICIALIZAÇÃO
# =====================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)