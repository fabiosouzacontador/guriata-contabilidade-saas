import requests
import json
from datetime import datetime

# ============================================
# CONFIGURAÇÃO
# ============================================

BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# Variáveis para armazenar IDs
user_id = None
escola_id = None
turma_id = None
aluno_id = None
conta_debito_id = None
conta_credito_id = None
lancamento_id = None

# ============================================
# CORES PARA OUTPUT
# ============================================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_section(title):
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}{title}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}\n")

# ============================================
# 1. TESTES DE USUARIOS
# ============================================

def test_users():
    global user_id
    print_section("1️⃣ TESTANDO USERS")
    
    # CREATE USER
    print_info("POST /api/users/ - Criando usuário...")
    user_data = {
        "email": "professor@guriata.com",
        "nome": "João Silva",
        "senha": "senha123",
        "eh_professor": True,
        "eh_admin": False
    }
    response = requests.post(f"{BASE_URL}/api/users/", json=user_data, headers=HEADERS)
    
    if response.status_code == 201:
        user_id = response.json()["id"]
        print_success(f"Usuário criado com ID: {user_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar usuário: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE SECOND USER
    print_info("\nPOST /api/users/ - Criando segundo usuário...")
    user_data2 = {
        "email": "aluno@guriata.com",
        "nome": "Maria Santos",
        "senha": "senha456",
        "eh_professor": False
    }
    response = requests.post(f"{BASE_URL}/api/users/", json=user_data2, headers=HEADERS)
    
    if response.status_code == 201:
        aluno_user_id = response.json()["id"]
        print_success(f"Segundo usuário criado com ID: {aluno_user_id}")
    else:
        print_error(f"Erro ao criar segundo usuário")
    
    # GET ALL USERS
    print_info("\nGET /api/users/ - Listando usuários...")
    response = requests.get(f"{BASE_URL}/api/users/", headers=HEADERS)
    
    if response.status_code == 200:
        users = response.json()
        print_success(f"Total de usuários: {len(users)}")
        for user in users:
            print(f"  - {user['nome']} ({user['email']}) [ID: {user['id']}]")
    else:
        print_error(f"Erro ao listar usuários")
    
    # GET USER BY ID
    print_info(f"\nGET /api/users/{user_id} - Obtendo usuário específico...")
    response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Usuário encontrado: {response.json()['nome']}")
    else:
        print_error(f"Erro ao obter usuário")
    
    # GET USER BY EMAIL
    print_info("\nGET /api/users/email/{email} - Obtendo por email...")
    response = requests.get(f"{BASE_URL}/api/users/email/professor@guriata.com", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Usuário encontrado por email: {response.json()['nome']}")
    else:
        print_error(f"Erro ao obter usuário por email")
    
    # UPDATE USER
    print_info(f"\nPUT /api/users/{user_id} - Atualizando usuário...")
    update_data = {
        "nome": "João Silva Atualizado"
    }
    response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Usuário atualizado: {response.json()['nome']}")
    else:
        print_error(f"Erro ao atualizar usuário")
    
    return True

# ============================================
# 2. TESTES DE ESCOLAS
# ============================================

def test_escolas():
    global escola_id
    print_section("2️⃣ TESTANDO ESCOLAS")
    
    # CREATE ESCOLA
    print_info("POST /api/escolas/ - Criando escola...")
    escola_data = {
        "nome": "Escola de Contabilidade Excellence",
        "descricao": "Instituição de ensino em contabilidade",
        "cnpj": "12.345.678/0001-90",
        "endereco": "Rua das Flores, 123",
        "telefone": "(11) 98765-4321",
        "email": "contato@escola.com",
        "criador_id": user_id
    }
    response = requests.post(f"{BASE_URL}/api/escolas/", json=escola_data, headers=HEADERS)
    
    if response.status_code == 201:
        escola_id = response.json()["id"]
        print_success(f"Escola criada com ID: {escola_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar escola: {response.status_code}")
        print(response.text)
        return False
    
    # GET ALL ESCOLAS
    print_info("\nGET /api/escolas/ - Listando escolas...")
    response = requests.get(f"{BASE_URL}/api/escolas/", headers=HEADERS)
    
    if response.status_code == 200:
        escolas = response.json()
        print_success(f"Total de escolas: {len(escolas)}")
        for escola in escolas:
            print(f"  - {escola['nome']} [ID: {escola['id']}]")
    else:
        print_error(f"Erro ao listar escolas")
    
    # GET ESCOLA BY ID
    print_info(f"\nGET /api/escolas/{escola_id} - Obtendo escola...")
    response = requests.get(f"{BASE_URL}/api/escolas/{escola_id}", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Escola encontrada: {response.json()['nome']}")
    else:
        print_error(f"Erro ao obter escola")
    
    # UPDATE ESCOLA
    print_info(f"\nPUT /api/escolas/{escola_id} - Atualizando escola...")
    update_data = {
        "nome": "Escola de Contabilidade Excellence - Atualizada",
        "telefone": "(11) 99999-9999"
    }
    response = requests.put(f"{BASE_URL}/api/escolas/{escola_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Escola atualizada: {response.json()['nome']}")
    else:
        print_error(f"Erro ao atualizar escola")
    
    return True

# ============================================
# 3. TESTES DE TURMAS
# ============================================

def test_turmas():
    global turma_id
    print_section("3️⃣ TESTANDO TURMAS")
    
    # CREATE TURMA
    print_info("POST /api/turmas/ - Criando turma...")
    turma_data = {
        "nome": "Contabilidade Básica - 2024/1",
        "descricao": "Turma de introdução à contabilidade",
        "periodo": "2024/1",
        "escola_id": escola_id,
        "professor_id": user_id
    }
    response = requests.post(f"{BASE_URL}/api/turmas/", json=turma_data, headers=HEADERS)
    
    if response.status_code == 201:
        turma_id = response.json()["id"]
        print_success(f"Turma criada com ID: {turma_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar turma: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE SECOND TURMA
    print_info("\nPOST /api/turmas/ - Criando segunda turma...")
    turma_data2 = {
        "nome": "Contabilidade Avançada - 2024/1",
        "descricao": "Turma avançada",
        "periodo": "2024/1",
        "escola_id": escola_id,
        "professor_id": user_id
    }
    response = requests.post(f"{BASE_URL}/api/turmas/", json=turma_data2, headers=HEADERS)
    
    if response.status_code == 201:
        print_success(f"Segunda turma criada")
    else:
        print_error(f"Erro ao criar segunda turma")
    
    # GET ALL TURMAS
    print_info("\nGET /api/turmas/ - Listando turmas...")
    response = requests.get(f"{BASE_URL}/api/turmas/", headers=HEADERS)
    
    if response.status_code == 200:
        turmas = response.json()
        print_success(f"Total de turmas: {len(turmas)}")
        for turma in turmas:
            print(f"  - {turma['nome']} [ID: {turma['id']}]")
    else:
        print_error(f"Erro ao listar turmas")
    
    # GET TURMAS BY ESCOLA
    print_info(f"\nGET /api/turmas/?escola_id={escola_id} - Filtrando por escola...")
    response = requests.get(f"{BASE_URL}/api/turmas/?escola_id={escola_id}", headers=HEADERS)
    
    if response.status_code == 200:
        turmas = response.json()
        print_success(f"Turmas da escola: {len(turmas)}")
    else:
        print_error(f"Erro ao filtrar turmas")
    
    # UPDATE TURMA
    print_info(f"\nPUT /api/turmas/{turma_id} - Atualizando turma...")
    update_data = {
        "nome": "Contabilidade Básica - 2024/1 - Turma A"
    }
    response = requests.put(f"{BASE_URL}/api/turmas/{turma_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Turma atualizada: {response.json()['nome']}")
    else:
        print_error(f"Erro ao atualizar turma")
    
    return True

# ============================================
# 4. TESTES DE ALUNOS
# ============================================

def test_alunos():
    global aluno_id
    print_section("4️⃣ TESTANDO ALUNOS")
    
    # CREATE ALUNO
    print_info("POST /api/alunos/ - Criando aluno...")
    aluno_data = {
        "matricula": "2024001",
        "nome": "Carlos Mendes",
        "email": "carlos@example.com",
        "cpf": "123.456.789-00",
        "turma_id": turma_id
    }
    response = requests.post(f"{BASE_URL}/api/alunos/", json=aluno_data, headers=HEADERS)
    
    if response.status_code == 201:
        aluno_id = response.json()["id"]
        print_success(f"Aluno criado com ID: {aluno_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar aluno: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE SECOND ALUNO
    print_info("\nPOST /api/alunos/ - Criando segundo aluno...")
    aluno_data2 = {
        "matricula": "2024002",
        "nome": "Ana Paula",
        "email": "ana@example.com",
        "cpf": "987.654.321-00",
        "turma_id": turma_id
    }
    response = requests.post(f"{BASE_URL}/api/alunos/", json=aluno_data2, headers=HEADERS)
    
    if response.status_code == 201:
        print_success(f"Segundo aluno criado")
    else:
        print_error(f"Erro ao criar segundo aluno")
    
    # GET ALL ALUNOS
    print_info("\nGET /api/alunos/ - Listando alunos...")
    response = requests.get(f"{BASE_URL}/api/alunos/", headers=HEADERS)
    
    if response.status_code == 200:
        alunos = response.json()
        print_success(f"Total de alunos: {len(alunos)}")
        for aluno in alunos:
            print(f"  - {aluno['nome']} (Matrícula: {aluno['matricula']}) [ID: {aluno['id']}]")
    else:
        print_error(f"Erro ao listar alunos")
    
    # GET ALUNOS BY TURMA
    print_info(f"\nGET /api/alunos/?turma_id={turma_id} - Alunos da turma...")
    response = requests.get(f"{BASE_URL}/api/alunos/?turma_id={turma_id}", headers=HEADERS)
    
    if response.status_code == 200:
        alunos = response.json()
        print_success(f"Alunos da turma: {len(alunos)}")
    else:
        print_error(f"Erro ao filtrar alunos")
    
    # GET ALUNO BY MATRICULA
    print_info("\nGET /api/alunos/matricula/{matricula} - Obtendo por matrícula...")
    response = requests.get(f"{BASE_URL}/api/alunos/matricula/2024001", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Aluno encontrado: {response.json()['nome']}")
    else:
        print_error(f"Erro ao obter aluno por matrícula")
    
    # UPDATE ALUNO
    print_info(f"\nPUT /api/alunos/{aluno_id} - Atualizando aluno...")
    update_data = {
        "nome": "Carlos Mendes Santos"
    }
    response = requests.put(f"{BASE_URL}/api/alunos/{aluno_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Aluno atualizado: {response.json()['nome']}")
    else:
        print_error(f"Erro ao atualizar aluno")
    
    return True

# ============================================
# 5. TESTES DE CONTAS
# ============================================

def test_contas():
    global conta_debito_id, conta_credito_id
    print_section("5️⃣ TESTANDO CONTAS")
    
    # CREATE CONTA DEBITO
    print_info("POST /api/contas/ - Criando conta de débito...")
    conta_debito_data = {
        "codigo": "1.1.1.01",
        "nome": "Caixa",
        "descricao": "Conta de caixa da empresa",
        "tipo": "ATIVO",
        "saldo_inicial": 10000.0,
        "escola_id": escola_id
    }
    response = requests.post(f"{BASE_URL}/api/contas/", json=conta_debito_data, headers=HEADERS)
    
    if response.status_code == 201:
        conta_debito_id = response.json()["id"]
        print_success(f"Conta débito criada com ID: {conta_debito_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar conta débito: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE CONTA CREDITO
    print_info("\nPOST /api/contas/ - Criando conta de crédito...")
    conta_credito_data = {
        "codigo": "2.1.1.01",
        "nome": "Fornecedores",
        "descricao": "Conta de fornecedores",
        "tipo": "PASSIVO",
        "saldo_inicial": 5000.0,
        "escola_id": escola_id
    }
    response = requests.post(f"{BASE_URL}/api/contas/", json=conta_credito_data, headers=HEADERS)
    
    if response.status_code == 201:
        conta_credito_id = response.json()["id"]
        print_success(f"Conta crédito criada com ID: {conta_credito_id}")
    else:
        print_error(f"Erro ao criar conta crédito: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE MORE CONTAS
    print_info("\nPOST /api/contas/ - Criando conta de receita...")
    contas_data = [
        {
            "codigo": "3.1.1.01",
            "nome": "Receita de Serviços",
            "descricao": "Receita de prestação de serviços",
            "tipo": "RECEITA",
            "saldo_inicial": 0.0,
            "escola_id": escola_id
        },
        {
            "codigo": "4.1.1.01",
            "nome": "Despesa Administrativa",
            "descricao": "Despesas administrativas",
            "tipo": "DESPESA",
            "saldo_inicial": 0.0,
            "escola_id": escola_id
        }
    ]
    
    for conta_data in contas_data:
        response = requests.post(f"{BASE_URL}/api/contas/", json=conta_data, headers=HEADERS)
        if response.status_code == 201:
            print_success(f"Conta criada: {conta_data['nome']}")
        else:
            print_error(f"Erro ao criar conta: {conta_data['nome']}")
    
    # GET ALL CONTAS
    print_info("\nGET /api/contas/ - Listando contas...")
    response = requests.get(f"{BASE_URL}/api/contas/", headers=HEADERS)
    
    if response.status_code == 200:
        contas = response.json()
        print_success(f"Total de contas: {len(contas)}")
        for conta in contas:
            print(f"  - {conta['codigo']} - {conta['nome']} ({conta['tipo']}) - Saldo: R$ {conta['saldo_atual']:.2f}")
    else:
        print_error(f"Erro ao listar contas")
    
    # GET CONTAS BY ESCOLA
    print_info(f"\nGET /api/contas/?escola_id={escola_id} - Contas da escola...")
    response = requests.get(f"{BASE_URL}/api/contas/?escola_id={escola_id}", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Total de contas da escola: {len(response.json())}")
    else:
        print_error(f"Erro ao filtrar contas")
    
    # GET CONTA BY CODIGO
    print_info("\nGET /api/contas/codigo/{codigo} - Obtendo por código...")
    response = requests.get(f"{BASE_URL}/api/contas/codigo/1.1.1.01", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Conta encontrada: {response.json()['nome']}")
    else:
        print_error(f"Erro ao obter conta por código")
    
    # UPDATE CONTA
    print_info(f"\nPUT /api/contas/{conta_debito_id} - Atualizando conta...")
    update_data = {
        "nome": "Caixa - Atualizado"
    }
    response = requests.put(f"{BASE_URL}/api/contas/{conta_debito_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Conta atualizada: {response.json()['nome']}")
    else:
        print_error(f"Erro ao atualizar conta")
    
    return True

# ============================================
# 6. TESTES DE LANCAMENTOS
# ============================================

def test_lancamentos():
    global lancamento_id
    print_section("6️⃣ TESTANDO LANÇAMENTOS")
    
    # CREATE LANCAMENTO
    print_info("POST /api/lancamentos/ - Criando lançamento...")
    lancamento_data = {
        "numero": "001/2024",
        "descricao": "Venda de serviços",
        "valor": 500.0,
        "conta_debito_id": conta_debito_id,
        "conta_credito_id": conta_credito_id,
        "turma_id": turma_id,
        "observacoes": "Primeiro lançamento de teste"
    }
    response = requests.post(
        f"{BASE_URL}/api/lancamentos/",
        json=lancamento_data,
        headers=HEADERS,
        params={"usuario_id": user_id}
    )
    
    if response.status_code == 201:
        lancamento_id = response.json()["id"]
        print_success(f"Lançamento criado com ID: {lancamento_id}")
        print(json.dumps(response.json(), indent=2, default=str))
    else:
        print_error(f"Erro ao criar lançamento: {response.status_code}")
        print(response.text)
        return False
    
    # CREATE SECOND LANCAMENTO
    print_info("\nPOST /api/lancamentos/ - Criando segundo lançamento...")
    lancamento_data2 = {
        "numero": "002/2024",
        "descricao": "Compra de materiais",
        "valor": 300.0,
        "conta_debito_id": conta_debito_id,
        "conta_credito_id": conta_credito_id,
        "turma_id": turma_id
    }
    response = requests.post(
        f"{BASE_URL}/api/lancamentos/",
        json=lancamento_data2,
        headers=HEADERS,
        params={"usuario_id": user_id}
    )
    
    if response.status_code == 201:
        print_success(f"Segundo lançamento criado")
    else:
        print_error(f"Erro ao criar segundo lançamento")
    
    # GET ALL LANCAMENTOS
    print_info("\nGET /api/lancamentos/ - Listando lançamentos...")
    response = requests.get(f"{BASE_URL}/api/lancamentos/", headers=HEADERS)
    
    if response.status_code == 200:
        lancamentos = response.json()
        print_success(f"Total de lançamentos: {len(lancamentos)}")
        for lanc in lancamentos:
            print(f"  - {lanc['numero']} - {lanc['descricao']} - R$ {lanc['valor']:.2f} - Status: {lanc['status']}")
    else:
        print_error(f"Erro ao listar lançamentos")
    
    # GET LANCAMENTOS BY TURMA
    print_info(f"\nGET /api/lancamentos/?turma_id={turma_id} - Lançamentos da turma...")
    response = requests.get(f"{BASE_URL}/api/lancamentos/?turma_id={turma_id}", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Lançamentos da turma: {len(response.json())}")
    else:
        print_error(f"Erro ao filtrar lançamentos")
    
    # GET LANCAMENTO BY ID
    print_info(f"\nGET /api/lancamentos/{lancamento_id} - Obtendo lançamento...")
    response = requests.get(f"{BASE_URL}/api/lancamentos/{lancamento_id}", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Lançamento encontrado: {response.json()['descricao']}")
    else:
        print_error(f"Erro ao obter lançamento")
    
    # UPDATE LANCAMENTO
    print_info(f"\nPUT /api/lancamentos/{lancamento_id} - Atualizando lançamento...")
    update_data = {
        "status": "APROVADO"
    }
    response = requests.put(f"{BASE_URL}/api/lancamentos/{lancamento_id}", json=update_data, headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"Lançamento atualizado - Status: {response.json()['status']}")
    else:
        print_error(f"Erro ao atualizar lançamento")
    
    return True

# ============================================
# 7. TESTES DE HEALTH CHECK
# ============================================

def test_health():
    print_section("7️⃣ TESTANDO HEALTH CHECK")
    
    print_info("GET /health - Verificando saúde da API...")
    response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
    
    if response.status_code == 200:
        print_success(f"API está saudável: {response.json()}")
    else:
        print_error(f"Erro ao verificar saúde da API")
    
    print_info("\nGET / - Obtendo informações da API...")
    response = requests.get(f"{BASE_URL}/", headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        print_success(f"API rodando com sucesso")
        print(json.dumps(data, indent=2, default=str))
    else:
        print_error(f"Erro ao obter informações da API")

# ============================================
# 8. RELATÓRIO FINAL
# ============================================

def print_summary():
    print_section("📊 RESUMO DOS TESTES")
    
    print(f"\n{Colors.BLUE}IDs criados durante os testes:{Colors.END}")
    print(f"  User ID: {user_id}")
    print(f"  Escola ID: {escola_id}")
    print(f"  Turma ID: {turma_id}")
    print(f"  Aluno ID: {aluno_id}")
    print(f"  Conta Débito ID: {conta_debito_id}")
    print(f"  Conta Crédito ID: {conta_credito_id}")
    print(f"  Lançamento ID: {lancamento_id}")
    
    print(f"\n{Colors.BLUE}URLs úteis:{Colors.END}")
    print(f"  Swagger UI: http://localhost:8000/docs")
    print(f"  ReDoc: http://localhost:8000/redoc")
    print(f"  Health: http://localhost:8000/health")
    
    print(f"\n{Colors.GREEN}Todos os testes foram executados com sucesso!{Colors.END}\n")

# ============================================
# EXECUTAR TODOS OS TESTES
# ============================================

def run_all_tests():
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}🧪 INICIANDO TESTES DA API GURIATA{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    try:
        test_health()
        test_users()
        test_escolas()
        test_turmas()
        test_alunos()
        test_contas()
        test_lancamentos()
        
        print_summary()
        
    except Exception as e:
        print_error(f"Erro geral durante os testes: {str(e)}")

if __name__ == "__main__":
    run_all_tests()
