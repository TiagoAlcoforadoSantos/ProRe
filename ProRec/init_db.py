import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    """Inicializa o banco de dados criando as tabelas e inserindo dados iniciais"""
    
    conn = sqlite3.connect('reciclo.db')
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK(perfil IN ('funcionario', 'cliente')),
            telefone TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
        
    # Tabela de residuos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS residuos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            nome_residuo TEXT NOT NULL,
            descricao TEXT,
            quantidade_total INTEGER NOT NULL DEFAULT 1,
            quantidade_disponivel INTEGER NOT NULL DEFAULT 1,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de reservas_residuos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas_residuo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            residuos_id INTEGER NOT NULL,
            data_retirada TIMESTAMP NOT NULL,
            data_devolucao TIMESTAMP,
            status TEXT NOT NULL CHECK(status IN ('ativa', 'devolvida')),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (residuos_id) REFERENCES residuos (id)
        )
    ''')
    
    # Insere usuários de exemplo
    senha_funcionario = generate_password_hash('admin123')
    senha_cliente = generate_password_hash('cliente123')
    #Funcionario=admin
    cursor.execute('''
        INSERT OR IGNORE INTO usuarios (nome, email, senha, perfil, telefone)
        VALUES 
        ('Admin reciclo', 'admin@email.com', ?, 'funcionario', '81987654321'),
        ('Maria Silva', 'maria@email.com', ?, 'cliente', '81912345678'),
        ('João Santos', 'joao@email.com', ?, 'cliente', '81998765432')
    ''', (senha_funcionario, senha_cliente, senha_cliente))
    
    # Insere residuos de exemplo
    cursor.execute('''
        INSERT OR IGNORE INTO residuos (categoria,nome_residuo,descricao,quantidade_total,quantidade_disponivel)
        VALUES 
        ('aluminio','latas','latas de refrigerante','20','20'),
        ('Plastico','Garrafas','garrafa pet','2','1')
    ''')
    
    conn.commit()
    conn.close()


if __name__ == '__main__':
    init_db()