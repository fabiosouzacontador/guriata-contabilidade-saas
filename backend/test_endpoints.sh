#!/bin/bash
echo "================================"
echo "🧪 TESTANDO API GURIATA"
echo "================================"
echo ""
echo "1️⃣ Health Check"
curl http://localhost:8000/health
echo -e "\n\n"
echo "2️⃣ Listar Usuários"
curl http://localhost:8000/api/users/
echo -e "\n\n"
echo "3️⃣ Listar Escolas"
curl http://localhost:8000/api/escolas/
echo -e "\n\n"
echo "4️⃣ Listar Turmas"
curl http://localhost:8000/api/turmas/
echo -e "\n\n"
echo "5️⃣ Listar Alunos"
curl http://localhost:8000/api/alunos/
echo -e "\n\n"
echo "6️⃣ Listar Contas"
curl http://localhost:8000/api/contas/
echo -e "\n\n"
echo "7️⃣ Listar Lançamentos"
curl http://localhost:8000/api/lancamentos/
echo -e "\n\n"
echo "================================"
echo "✅ Testes Concluídos!"
echo "================================"
