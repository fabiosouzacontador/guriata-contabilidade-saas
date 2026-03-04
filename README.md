# 🎓 Guriata Contabilidade SaaS

> **Sistema com IA Tutor para Educação Contabil**

Uma plataforma SaaS inovadora que integra lançamentos contábeis, IA Tutor educativa e relatórios automáticos. Ideal para universidades, escolas técnicas e cursos de contabilidade.

## ✨ Diferenciais

- 🤖 **IA Tutor Inteligente**: Alunos aprendem contabilidade praticando com sugestões inteligentes
- 📊 **Relatórios Automáticos**: Balancete, DRE e análises em tempo real
- 📚 **Multi-Empresa**: Suporte para múltiplas escolas/universidades simultaneamente
- 🔐 **LGPD-Compliant**: Segurança e privacidade desde a base
- 🚀 **Escalável**: Pronto para crescer de 1 a 10.000+ usuários
- 💰 **SaaS B2B**: Modelo de assinatura mensal ou anual

## 🎯 Público-Alvo

- Universidades (cursos de Contabilidade)
- Escolas técnicas (técnico em contabilidade)
- Cursos profissionalizantes e livres
- Institutos de educação profissional

## 🚀 Quick Start

### Pré-requisitos
- Python 3.9+
- Node.js 16+
- Docker e Docker Compose
- PostgreSQL (ou usar via Docker)

### Setup Local (Com Docker)

```bash
# 1. Clone o repositório
git clone https://github.com/fabiosouzacontador/guriata-contabilidade-saas.git
cd guriata-contabilidade-saas

# 2. Suba os serviços (PostgreSQL + Backend + Frontend)
docker-compose up -d

# 3. Inicialize o banco de dados
docker-compose exec backend python app/init_db.py

# 4. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend (Docs): http://localhost:8000/docs
```

### Setup Local (Sem Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edite .env com suas configurações
python main.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

## 📋 Roadmap (1-3 meses)

### Semana 1-2: Estrutura e Infra
- [x] Estruturação do repositório
- [ ] Setup Heroku + PostgreSQL
- [ ] CI/CD básico (GitHub Actions)

### Semana 3-4: Autenticação
- [ ] Cadastro e login de usuários
- [ ] Autenticação JWT
- [ ] Multi-tenant (múltiplas escolas)

### Semana 4-5: Lançamentos Contábeis
- [ ] CRUD de lançamentos
- [ ] Validações contábeis
- [ ] Isolamento por empresa

### Semana 5-6: Relatórios
- [ ] Balancete
- [ ] DRE (Demonstração de Resultado)
- [ ] Exportação (PDF/Excel)

### Semana 6-7: IA Tutor
- [ ] FAQ educativa
- [ ] Sugestões automáticas
- [ ] Chat com alunos

### Semana 7-8: Frontend
- [ ] Páginas de login/cadastro
- [ ] Dashboard
- [ ] Formulários de lançamentos
- [ ] Visualização de relatórios
- [ ] Chat com IA Tutor

### Semana 8-12: Preparação para Venda
- [ ] Landing page
- [ ] Integração de pagamentos
- [ ] Testes com usuários reais
- [ ] Onboarding e suporte

## 📁 Estrutura do Projeto

```
backend/          # API FastAPI + PostgreSQL
frontend/         # Interface web (React)
docs/            # Documentação
scripts/         # Scripts auxiliares
.github/         # Workflows de CI/CD
```

## 🛠️ Stack Tecnológico

**Backend:**
- FastAPI (framework web moderno, rápido e fácil)
- SQLAlchemy (ORM para banco de dados)
- Pydantic (validação de dados)
- PyJWT (autenticação)
- PostgreSQL (banco de dados)

**Frontend:**
- React (interface interativa)
- Axios (chamadas HTTP)
- React Router (navegação)
- Tailwind CSS (estilos)

**Infraestrutura:**
- Docker (containerização)
- Heroku (hospedagem inicial)
- GitHub Actions (CI/CD)

## 📚 Documentação

- [Setup Local](docs/SETUP.md)
- [Documentação da API](docs/API.md)
- [Deploy e Infraestrutura](docs/DEPLOYMENT.md)
- [Esquema do Banco](docs/DATABASE.md)
- [Como Contribuir](CONTRIBUTING.md)

## 📞 Contato e Suporte

- Issues: [GitHub Issues](https://github.com/fabiosouzacontador/guriata-contabilidade-saas/issues)
- Email: seu-email@example.com
- Website: (em breve)

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

**Desenvolvido com ❤️ por Fabio Souza Contador**