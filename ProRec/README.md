# Reciclo - Plataforma de Sustentabilidade e Reciclagem

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Reciclo** é uma plataforma web de sustentabilidade e reciclagem construída com Flask, projetada para conectar produtores de materiais recicláveis, curadores que revisam submissões e administradores que gerenciam o sistema.

## 📋 Índice

- [Características](#características)
- [Arquitetura](#arquitetura)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelos de Dados](#modelos-de-dados)
- [Rotas e Blueprints](#rotas-e-blueprints)
- [Autenticação e Permissões](#autenticação-e-permissões)
- [Frontend](#frontend)
- [Desenvolvimento](#desenvolvimento)
- [Credenciais de Teste](#credenciais-de-teste)

## ✨ Características

### Sistema de Três Papéis

#### 👤 Produtor (Tipo 3)
- Publicar materiais recicláveis para coleta
- Visualizar histórico de coletas e pontos ganhos
- Sistema de conquistas e badges
- Mapa interativo de pontos de coleta
- Acompanhamento de eventos ao vivo

#### 🔍 Curador (Tipo 2)
- Revisar materiais submetidos por produtores
- Aprovar ou rejeitar submissões com feedback
- Dashboard de estatísticas de revisão
- Histórico de aprovações/rejeições

#### 🛡️ Administrador (Tipo 1)
- Gerenciar espaços físicos (pontos de coleta, eventos, cursos)
- Criar e agendar eventos no calendário
- Aprovar novos usuários cadastrados
- Gerenciar todos os usuários do sistema
- Acesso completo a todas as funcionalidades

## 🏗️ Arquitetura

### Stack Tecnológico

- **Backend**: Flask 3.0.0 (Python)
- **ORM**: Flask-SQLAlchemy
- **Autenticação**: Flask-Login
- **Formulários**: Flask-WTF + WTForms
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Frontend**: Jinja2 Templates + Tailwind CSS + Alpine.js
- **Migrações**: Flask-Migrate (Alembic)

### Padrões de Design

- **Application Factory Pattern**: Criação modular da aplicação via `create_app()`
- **Blueprints**: Organização modular de rotas por domínio
- **Role-Based Access Control (RBAC)**: Decoradores para controle de acesso
- **Repository Pattern**: Separação de lógica de negócio e acesso a dados
- **MVC Architecture**: Model-View-Controller para organização de código

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <repository-url>
cd ProRec
```

2. **Crie um ambiente virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o .env com suas configurações
# Altere pelo menos a SECRET_KEY para produção
```

5. **Inicialize o banco de dados**
```bash
python init_db_new.py
```

6. **Execute a aplicação**
```bash
python app.py
```

A aplicação estará disponível em: **http://127.0.0.1:5000**

## 🚀 Uso

### Login

Acesse http://127.0.0.1:5000 e faça login com uma das credenciais de teste:

- **Produtor**: produtor@reciclo.com / senha123
- **Curador**: curador@reciclo.com / senha123
- **Administrador**: admin@reciclo.com / senha123

### Fluxo de Trabalho

1. **Produtor publica material**
   - Acessa dashboard → aba "Publicar"
   - Preenche formulário (nome, categoria, descrição, localização)
   - Material criado com status "pendente"

2. **Curador revisa material**
   - Acessa dashboard → vê materiais pendentes
   - Aprova ou rejeita com feedback
   - Status do material atualizado

3. **Sistema de pontos e conquistas**
   - Coletas completadas geram pontos
   - Pontos desbloqueiam conquistas
   - Histórico visível no dashboard do produtor

4. **Administrador gerencia sistema**
   - Cria espaços físicos de coleta
   - Agenda eventos e cursos
   - Aprova novos usuários

## 📁 Estrutura do Projeto

```
ProRec/
├── app.py                      # Application factory e ponto de entrada
├── config.py                   # Configurações por ambiente (dev/prod/test)
├── extensions.py               # Inicialização de extensões Flask
├── requirements.txt            # Dependências Python
├── .env.example                # Template de variáveis de ambiente
├── init_db_new.py              # Script de inicialização do banco com seed data
├── add_mock_data.py            # Script para adicionar dados de teste extras
├── view_db.py                  # Script para visualizar dados do banco
├── reciclo.db                  # Banco SQLite (gerado automaticamente)
│
├── models/                     # Modelos de dados (SQLAlchemy)
│   ├── __init__.py             # Exporta todos os modelos
│   ├── user.py                 # Modelo User + Notificacao
│   ├── material.py             # Modelo Material (materiais recicláveis)
│   ├── space.py                # Modelo Space (pontos de coleta)
│   ├── event.py                # Modelo Event (eventos)
│   └── achievement.py          # Modelos Achievement e Collection
│
├── routes/                     # Blueprints Flask
│   ├── __init__.py
│   ├── auth.py                 # Rotas de autenticação (login/logout)
│   ├── producer.py             # Rotas do dashboard produtor
│   ├── curator.py              # Rotas do dashboard curador
│   ├── admin.py                # Rotas do dashboard admin
│   └── api.py                  # API REST endpoints (todos os dashboards)
│
├── decorators/                 # Decoradores customizados
│   ├── __init__.py
│   └── auth.py                 # Decoradores de autorização
│
├── templates/                  # Templates Jinja2
│   ├── base.html               # Template base com header/footer
│   ├── auth/
│   │   └── login.html          # Página de login
│   ├── producer/
│   │   └── dashboard.html      # Dashboard produtor (3 abas) - integrado com API
│   ├── curator/
│   │   └── dashboard.html      # Dashboard curador - integrado com API
│   ├── admin/
│   │   └── dashboard.html      # Dashboard admin (3 abas) - integrado com API
│   └── errors/
│       ├── 403.html            # Acesso negado
│       ├── 404.html            # Página não encontrada
│       └── 500.html            # Erro interno
│
└── static/                     # Arquivos estáticos (futuro)
    ├── css/
    ├── js/
    └── images/
```

## 🔍 Visualizando o Banco de Dados

### Opção 1: DB Browser for SQLite (Recomendado)

1. Baixe e instale o **DB Browser for SQLite**: https://sqlitebrowser.org/dl/
2. Abra o arquivo: `ProRec/reciclo.db`
3. Navegue pelas tabelas na aba "Browse Data"

### Opção 2: Extensão VSCode

1. Instale a extensão **SQLite Viewer** ou **SQLite** no VSCode
2. Clique no arquivo `reciclo.db` para abrir o visualizador

### Opção 3: Script Python

```bash
python view_db.py
```

Este script exibe todas as tabelas e dados no terminal.

### Opção 4: SQLite CLI

```bash
cd ProRec
sqlite3 reciclo.db
.tables
SELECT * FROM users;
SELECT * FROM materials;
.quit
```

## 🗄️ Modelos de Dados

### User Model

```python
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Identificação
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Perfil
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(150))

    # Sistema de Roles
    tipo = db.Column(db.Integer, default=TipoUsuario.PRODUCER.value)
    # 1 = Admin, 2 = Curator, 3 = Producer

    # Status
    status = db.Column(db.String(10), default=StatusUsuario.PENDENTE.value)
    # 'ativo', 'inativo', 'pendente'

    # Gamificação (Produtores)
    pontos = db.Column(db.Integer, default=0)

    # Timestamps
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    ultima_atividade = db.Column(db.DateTime, default=datetime.utcnow)

    # Flags
    is_active = db.Column(db.Boolean, default=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
```

### Enums

```python
class TipoUsuario(int, Enum):
    ADMIN = 1
    CURATOR = 2
    PRODUCER = 3

class StatusUsuario(str, Enum):
    ATIVO = 'ativo'
    INATIVO = 'inativo'
    PENDENTE = 'pendente'
```

### Material Model

```python
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    # 'plastico', 'vidro', 'papel', 'metal', 'eletronicos', 'organico'
    descricao = db.Column(db.Text)
    localizacao = db.Column(db.String(300), nullable=False)
    quantidade = db.Column(db.String(100))

    # Status de revisão
    status = db.Column(db.String(20), default='pending')
    # 'pending', 'approved', 'rejected'
    feedback = db.Column(db.Text)
    pontos_concedidos = db.Column(db.Integer, default=0)

    # Relacionamentos
    produtor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    curador_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    revisado_em = db.Column(db.DateTime)
```

### Space Model

```python
class Space(db.Model):
    __tablename__ = 'spaces'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(20), default='coleta')
    # 'coleta', 'evento', 'curso'
    endereco = db.Column(db.String(300), nullable=False)
    horario = db.Column(db.String(100))
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
```

### Event Model

```python
class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(20), default='coleta')
    # 'coleta', 'evento', 'curso', 'workshop'
    status = db.Column(db.String(20), default='agendado')
    # 'agendado', 'em_andamento', 'concluido', 'cancelado'
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime)
    horario = db.Column(db.String(50))
    espaco_id = db.Column(db.Integer, db.ForeignKey('spaces.id'))
    localizacao_custom = db.Column(db.String(300))
```

### Achievement Model

```python
class Achievement(db.Model):
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    icone = db.Column(db.String(10), nullable=False)  # Emoji
    pontos_necessarios = db.Column(db.Integer, default=0)
    ordem = db.Column(db.Integer, default=0)
```

### Collection Model (Histórico de Coletas)

```python
class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    material_nome = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    quantidade = db.Column(db.String(100))
    pontos = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text)
    produtor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'))
    data_coleta = db.Column(db.DateTime, default=datetime.utcnow)
```

## 🛣️ Rotas e Blueprints

### Auth Blueprint (`/`)

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Redireciona para login |
| `/login` | GET, POST | Página de login |
| `/logout` | GET | Logout do usuário |

### Producer Blueprint (`/produtor`)

| Rota | Método | Descrição | Decorador |
|------|--------|-----------|-----------|
| `/produtor/` | GET | Dashboard produtor | `@producer_required` |

### Curator Blueprint (`/curador`)

| Rota | Método | Descrição | Decorador |
|------|--------|-----------|-----------|
| `/curador/` | GET | Dashboard curador | `@curator_required` |

### Admin Blueprint (`/admin`)

| Rota | Método | Descrição | Decorador |
|------|--------|-----------|-----------|
| `/admin/` | GET | Dashboard admin | `@admin_required` |

### API Blueprint (`/api`)

#### Producer Endpoints

| Rota | Método | Descrição |
|------|--------|-----------|
| `/api/producer/stats` | GET | Estatísticas do dashboard (pontos, coletas, conquistas) |
| `/api/producer/achievements` | GET | Lista de conquistas com status de desbloqueio |
| `/api/producer/collections` | GET | Histórico de coletas do produtor |
| `/api/producer/materials` | GET | Materiais publicados pelo produtor |
| `/api/producer/materials` | POST | Publicar novo material |
| `/api/producer/collection-points` | GET | Pontos de coleta disponíveis |
| `/api/producer/events/today` | GET | Eventos acontecendo hoje |

#### Curator Endpoints

| Rota | Método | Descrição |
|------|--------|-----------|
| `/api/curator/stats` | GET | Estatísticas (pendentes, aprovados hoje, rejeitados hoje) |
| `/api/curator/pending-materials` | GET | Materiais aguardando revisão |
| `/api/curator/review-history` | GET | Histórico de revisões do curador |
| `/api/curator/materials/<id>/approve` | POST | Aprovar material (com feedback e pontos) |
| `/api/curator/materials/<id>/reject` | POST | Rejeitar material (requer feedback) |

#### Admin Endpoints

| Rota | Método | Descrição |
|------|--------|-----------|
| `/api/admin/stats` | GET | Estatísticas gerais do sistema |
| `/api/admin/spaces` | GET | Lista todos os espaços |
| `/api/admin/spaces` | POST | Criar novo espaço |
| `/api/admin/spaces/<id>` | PUT | Atualizar espaço |
| `/api/admin/events` | GET | Próximos eventos |
| `/api/admin/events` | POST | Criar novo evento |
| `/api/admin/pending-users` | GET | Usuários aguardando aprovação |
| `/api/admin/active-users` | GET | Usuários ativos do sistema |
| `/api/admin/users/<id>/approve` | POST | Aprovar usuário pendente |
| `/api/admin/users/<id>/reject` | POST | Rejeitar usuário pendente |
| `/api/admin/users/<id>` | PUT | Atualizar dados do usuário |

#### Exemplos de Uso da API

**Publicar Material (Producer):**
```javascript
fetch('/api/producer/materials', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        name: 'Garrafas PET',
        category: 'plastico',
        description: '20 garrafas limpas',
        location: 'Rua das Flores, 123'
    })
});
```

**Aprovar Material (Curator):**
```javascript
fetch('/api/curator/materials/1/approve', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({
        feedback: 'Material em excelente estado!',
        points: 50
    })
});
```

**Aprovar Usuário (Admin):**
```javascript
fetch('/api/admin/users/5/approve', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
    }
});
```

## 🔐 Autenticação e Permissões

### Decoradores de Autorização

```python
# Requer tipo específico
@admin_required       # Apenas tipo = 1
@curator_required     # Apenas tipo = 2
@producer_required    # Apenas tipo = 3

# Requer estar ativo
@active_user_required

# Múltiplos tipos permitidos
@user_type_required([1, 2])  # Admin ou Curator
```

### Exemplo de Uso

```python
@producer_bp.route('/')
@login_required
@producer_required
@active_user_required
def dashboard():
    return render_template('producer/dashboard.html')
```

### Lógica de Redirecionamento

Após login bem-sucedido, usuários são redirecionados baseado em `user.tipo`:
- Tipo 1 (Admin) → `/admin/`
- Tipo 2 (Curator) → `/curador/`
- Tipo 3 (Producer) → `/produtor/`

### Proteção de Rotas

- Todas as rotas exceto `/login` requerem autenticação
- Tentativa de acesso sem permissão → 403 Forbidden
- Usuário não autenticado → Redirect para `/login`

## 🎨 Frontend

### Tecnologias

- **Jinja2**: Template engine do Flask
- **Tailwind CSS**: Framework CSS utility-first
- **Alpine.js**: JavaScript reativo para interatividade

### Estrutura de Templates

#### base.html
Template base com:
- Header responsivo com nome do usuário e tipo
- Sistema de mensagens flash (sucesso/erro/info/warning)
- Link de logout
- CDN para Tailwind e Alpine.js

#### Dashboards

Todos os dashboards seguem o mesmo padrão:
- Layout responsivo com Tailwind
- Componentes Alpine.js para estado local
- Dados mockados para prototipagem
- Preparados para integração com API

### Componentes Alpine.js

#### Producer Dashboard
```javascript
function producerDashboard() {
    return {
        tab: 'history',          // Aba ativa
        showForm: false,         // Toggle formulário
        formData: {...},         // Dados do formulário
        publishedItems: [...],   // Materiais publicados
        submitMaterial() {...}   // Submissão de material
    }
}
```

#### Curator Dashboard
```javascript
function curatorDashboard() {
    return {
        pendingMaterials: [...],
        approveMaterial(id) {...},
        rejectMaterial(id) {...}
    }
}
```

#### Admin Dashboard
```javascript
function adminDashboard() {
    return {
        tab: 'spaces',           // Abas: spaces/calendar/users
        spaces: [...],
        upcomingEvents: [...],
        approveUser(id) {...}
    }
}
```

### Color Scheme

- **Primary**: `green-600` (#16a34a) - Tema sustentabilidade
- **Secondary**: `gray-*` - Elementos neutros
- **Accent**: `yellow-500/600` - Pontos e conquistas
- **Status Colors**:
  - Pendente: `yellow-600`
  - Aprovado: `green-600`
  - Rejeitado: `red-600`
  - Admin: `purple-600`
  - Curator: `blue-600`
  - Producer: `green-600`

## 💻 Desenvolvimento

### Configuração de Ambiente

O projeto usa três ambientes configurados em `config.py`:

#### Development (Padrão)
```python
FLASK_ENV=development
DEBUG=True
DATABASE: SQLite local
```

#### Production
```python
FLASK_ENV=production
DEBUG=False
DATABASE: PostgreSQL (configurar DATABASE_URL)
```

#### Testing
```python
FLASK_ENV=testing
TESTING=True
DATABASE: SQLite em memória
```

### Comandos Úteis

```bash
# Executar aplicação em modo debug
python app.py

# Executar em modo produção
FLASK_ENV=production python app.py

# Reinicializar banco de dados
rm instance/reciclo.db
python init_db_new.py

# Instalar dependências
pip install -r requirements.txt

# Gerar requirements.txt
pip freeze > requirements.txt
```

### Desenvolvimento Local

1. **Ativar ambiente virtual**
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. **Executar em modo debug**
```bash
python app.py
```

3. **Acessar**
- URL: http://127.0.0.1:5000
- Apenas localhost (segurança)

### Adicionando Novos Recursos

#### 1. Criar Modelo
```python
# models/material.py
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    # ... outros campos
```

#### 2. Criar Formulário
```python
# forms/material.py
class MaterialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    categoria = SelectField('Categoria', choices=[...])
    submit = SubmitField('Publicar')
```

#### 3. Criar Rota
```python
# routes/producer.py
@producer_bp.route('/publicar', methods=['GET', 'POST'])
@login_required
@producer_required
def publicar():
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material(
            nome=form.nome.data,
            produtor_id=current_user.id
        )
        db.session.add(material)
        db.session.commit()
        flash('Material publicado com sucesso!', 'success')
        return redirect(url_for('producer.dashboard'))
    return render_template('producer/publicar.html', form=form)
```

#### 4. Criar Template
```html
<!-- templates/producer/publicar.html -->
{% extends 'base.html' %}
{% block content %}
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.nome.label }} {{ form.nome }}
    {{ form.submit }}
</form>
{% endblock %}
```

### Debugging

#### Flask Debug Mode
```python
# app.py já configurado com debug=True em development
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
```

#### Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.debug('Debug message')
app.logger.info('Info message')
app.logger.error('Error message')
```

#### Interactive Shell
```bash
flask shell
>>> from models.user import User
>>> User.query.all()
```

## 🔑 Credenciais de Teste

### Usuários Pré-configurados

| Tipo | Email | Senha | Pontos | Status |
|------|-------|-------|--------|--------|
| **Administrador** | admin@reciclo.com | senha123 | 0 | Ativo |
| **Curador** | curador@reciclo.com | senha123 | 0 | Ativo |
| **Produtor** | produtor@reciclo.com | senha123 | 370 | Ativo |
| Produtor | joao@email.com | senha123 | 0 | Pendente |
| Produtor | maria@email.com | senha123 | 0 | Pendente |

### Seed Data Incluído

O script `init_db_new.py` cria os seguintes dados de exemplo:

| Tabela | Quantidade | Descrição |
|--------|------------|-----------|
| **Users** | 5 | 3 ativos (admin, curator, producer) + 2 pendentes |
| **Achievements** | 4 | Primeira Coleta, Eco Warrior, Guardião Verde, Mestre da Reciclagem |
| **Spaces** | 5 | 3 pontos de coleta + 1 auditório + 1 centro de treinamento |
| **Events** | 3 | Coleta de eletrônicos, Workshop, Feira de sustentabilidade |
| **Materials** | 3 | 1 aprovado, 1 pendente, 1 rejeitado |
| **Collections** | 3 | Histórico de coletas do produtor teste |

### Resetar Banco de Dados

```bash
# Windows (PowerShell)
Remove-Item reciclo.db
python init_db_new.py

# Windows (CMD)
del reciclo.db
python init_db_new.py

# Linux/Mac
rm reciclo.db
python init_db_new.py
```

### Visualizar Dados

```bash
# Via script Python
python view_db.py

# Via SQLite CLI
sqlite3 reciclo.db ".tables"
sqlite3 reciclo.db "SELECT * FROM users;"
```

### Adicionar Dados de Teste (Mock Data)

O script `add_mock_data.py` permite adicionar dados de teste adicionais a um banco de dados existente, sem precisar resetá-lo:

```bash
# Modo interativo (menu de opções)
python add_mock_data.py

# Adicionar todos os dados de uma vez
python add_mock_data.py --all
```

#### Modo Interativo

O menu interativo oferece as seguintes opções:

| Opção | Descrição | Quantidade |
|-------|-----------|------------|
| 1 | Adicionar usuários produtores | 5 |
| 2 | Adicionar materiais | 15 |
| 3 | Adicionar coletas (histórico) | 10 |
| 4 | Adicionar eventos | 5 |
| 5 | Adicionar espaços | 3 |
| 6 | Adicionar TODOS os dados | Todos acima |
| 7 | Ver estatísticas do banco | - |
| 0 | Sair | - |

#### Dados Gerados

O script gera dados realistas incluindo:

- **Usuários**: Nomes brasileiros aleatórios (Ana, Carlos, Beatriz, etc.)
- **Materiais**: Tipos variados (PET, papelão, vidro, eletrônicos, orgânicos)
- **Localizações**: Endereços fictícios em diferentes bairros
- **Eventos**: Coletas, workshops, cursos e feiras
- **Espaços**: Ecopontos, centros de reciclagem e salas de eventos

## 📝 Roadmap

### ✅ Fase 1: Fundação (Completo)
- [x] Application factory pattern
- [x] Blueprints (auth, producer, curator, admin)
- [x] Modelo User com roles
- [x] Sistema de autenticação
- [x] Decoradores de autorização
- [x] Templates base e dashboards
- [x] Error handlers (403, 404, 500)

### ✅ Fase 2: Modelos Core (Completo)
- [x] Modelo Material (materiais recicláveis)
- [x] Modelo Collection (histórico de coletas)
- [x] Modelo Achievement (conquistas/badges)
- [x] Modelo Space (pontos de coleta)
- [x] Modelo Event (eventos/agendamentos)
- [x] Seed data para desenvolvimento

### ✅ Fase 3: API Producer (Completo)
- [x] Endpoints para publicar materiais
- [x] Listagem de materiais do produtor
- [x] Listagem de pontos de coleta
- [x] Listagem de eventos do dia
- [x] Sistema de conquistas integrado
- [x] Histórico de coletas

### ✅ Fase 4: API Curator (Completo)
- [x] Endpoints de aprovação/rejeição
- [x] Listagem de materiais pendentes
- [x] Histórico de revisões
- [x] Sistema de pontos automático

### ✅ Fase 5: API Admin (Completo)
- [x] CRUD de espaços físicos
- [x] CRUD de eventos
- [x] Aprovação de usuários
- [x] Gerenciamento de usuários
- [x] Dashboard de estatísticas

### ✅ Fase 6: Integração Frontend-Backend (Completo)
- [x] Dashboard Producer integrado com API
- [x] Dashboard Curator integrado com API
- [x] Dashboard Admin integrado com API
- [x] Formulários funcionais com validação
- [x] Feedback visual de ações

### 🚧 Fase 7: Melhorias (Próximo)
- [ ] Upload de imagens para materiais
- [ ] Mapa interativo real (Leaflet/Google Maps)
- [ ] Calendário interativo (FullCalendar)
- [ ] Notificações em tempo real
- [ ] Ranking de produtores

### 📋 Fase 8: Testes
- [ ] Testes unitários (pytest)
- [ ] Testes de integração
- [ ] Testes de autorização
- [ ] Cobertura de código >80%

### 📋 Fase 9: Deploy
- [ ] Configuração PostgreSQL
- [ ] Docker/Docker Compose
- [ ] CI/CD Pipeline
- [ ] Documentação de deploy
- [ ] Monitoramento e logs

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Equipe Reciclo** - Desenvolvimento inicial

## 🙏 Agradecimentos

- Inspirado na necessidade real de conectar produtores de materiais recicláveis com curadores e pontos de coleta
- Design baseado em princípios de sustentabilidade e economia circular
- Comunidade Flask por ferramentas excelentes

---

**Reciclo** - Transformando reciclagem em impacto positivo 🌱♻️
