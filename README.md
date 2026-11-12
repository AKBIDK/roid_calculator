# ROI Calculator & Decision Copilot

Sistema empresarial de alta fidelidade para cálculo, simulação de sensibilidade e governança de retorno sobre investimento (ROI) em projetos estratégicos.

## Arquitetura da Solução
- **Motor Financeiro**: Cálculo exato de VPL, TIR (via convergência Newton-Raphson/Bisseção com tratamento de borda), Payback Simples e Descontado com interpolação linear, e Simulação de Monte Carlo.
- **Backend**: FastAPI (Python) com validação estrita via Pydantic e persistência relacional (PostgreSQL / SQLite para testes locais).
- **Frontend**: Aplicação React com Wizard guiado em 4 etapas e Dashboard de Indicadores Executivos.
- **Segurança e Hardening**: RBAC (Viewer, Editor, Admin), logs de auditoria imutáveis, imagens Docker com usuários não-root e `cap_drop: [ALL]`.

## Como Executar

### 1. Testes Automatizados Locais
Para rodar a suíte de testes unitários do motor financeiro sem dependências externas:
```bash
python3 -m unittest discover -s backend/tests -p "test_*.py"
```

### 2. Execução com Docker Compose
```bash
cp .env.example .env
docker-compose up --build -d
```
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API Docs (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
