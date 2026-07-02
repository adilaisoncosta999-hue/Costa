# Costa Workforce Manager (CWM) — Backend

Sistema SaaS multiempresa de controlo de assiduidade por QR Code.
Backend em **Django + Django REST Framework**, base de dados **PostgreSQL**.

> Este é o backend (API). A aplicação Android (Flutter) e o painel web são as próximas fases do projeto.

## 1. Estrutura do projeto

```
backend/
├── cwm/                    # Configurações do projeto (settings, urls)
├── apps/
│   ├── accounts/           # Utilizadores, papéis (roles), login/JWT
│   ├── companies/          # Empresas, departamentos, cargos, horários (multiempresa)
│   ├── employees/          # Funcionários, fotos, QR Code
│   └── attendance/         # Check-in/check-out, atrasos, relatórios PDF/Excel, dashboard
├── manage.py
├── requirements.txt
└── .env.example
```

## 2. Instalação (no teu computador)

Pré-requisitos: Python 3.11+, PostgreSQL 14+ instalados.

```bash
# 1. Criar ambiente virtual
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variáveis de ambiente
cp .env.example .env
# edita o .env com a password da tua base de dados

# 4. Criar a base de dados no PostgreSQL
psql -U postgres -c "CREATE DATABASE cwm_db;"
psql -U postgres -c "CREATE USER cwm_user WITH PASSWORD 'changeme';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE cwm_db TO cwm_user;"

# 5. Aplicar as migrações
python manage.py makemigrations
python manage.py migrate

# 6. Criar dados de demonstração (1 empresa, admins e 3 funcionários com QR Code)
python manage.py seed_demo

# 7. Correr o servidor
python manage.py runserver
```

A API fica disponível em `http://127.0.0.1:8000/api/` e o painel admin em `http://127.0.0.1:8000/admin/`.

## 3. Utilizadores de demonstração

| Username | Password    | Papel              |
|----------|-------------|--------------------|
| admin    | Admin#2026  | Super Admin (SaaS) |
| gestor   | Gestor#2026 | Admin da empresa   |

## 4. Principais endpoints da API

| Método | Endpoint                              | Descrição                                  |
|--------|----------------------------------------|---------------------------------------------|
| POST   | `/api/auth/login/`                    | Login (devolve access + refresh token)      |
| POST   | `/api/auth/refresh/`                  | Renovar token de acesso                     |
| GET/POST | `/api/companies/`                   | Gestão de empresas (só super_admin)         |
| GET/POST | `/api/departments/`                 | Departamentos                                |
| GET/POST | `/api/employees/`                   | Funcionários (gera QR Code automaticamente) |
| POST   | `/api/attendance/scan/`               | **Check-in/check-out via leitura do QR Code**|
| GET    | `/api/attendance/records/`            | Histórico de presenças                       |
| GET    | `/api/attendance/dashboard/`          | Estatísticas em tempo real                   |
| GET    | `/api/attendance/reports/export/?format=pdf` ou `excel` | Exportar relatório    |
| POST/GET | `/api/attendance/justifications/`   | Justificação de faltas                       |

### Exemplo: login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "gestor", "password": "Gestor#2026"}'
```

### Exemplo: marcar presença (check-in/check-out)

```bash
curl -X POST http://127.0.0.1:8000/api/attendance/scan/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"qr_token": "<token-lido-do-qr-code>", "latitude": -8.83, "longitude": 13.23}'
```

A primeira chamada do dia regista a **entrada**; a segunda regista a **saída**. O sistema calcula automaticamente atrasos e saídas antecipadas com base no horário (`WorkSchedule`) do funcionário.

## 5. Multiempresa (SaaS)

Todos os modelos principais (`Department`, `Position`, `Employee`, `AttendanceRecord`, etc.) têm uma chave estrangeira `company`. Os dados de cada empresa estão isolados automaticamente através do `CompanyScopedMixin` — cada utilizador só vê os dados da sua própria empresa, exceto o `super_admin`, que gere o SaaS por inteiro.

## 6. Próximas fases (já planeadas)

- **Fase 2** — Painel administrativo web (templates Django ou React) com leitor de QR Code via webcam.
- **Fase 3** — Aplicação Android em Flutter: login, scanner de QR Code, histórico, modo offline.
- **Fase 4** — Reconhecimento facial, notificações, integração com folha de salários, assinaturas/pagamentos.

## 7. Notas importantes

- Este código é um **MVP funcional**, pensado para correres e testares localmente. Para produção, é necessário: trocar `SECRET_KEY`, configurar `DEBUG=False`, usar HTTPS, configurar `ALLOWED_HOSTS`, e colocar `media/` num storage (ex: S3) em vez do disco local.
- O campo `qr_token` de cada funcionário é o valor codificado no QR Code do cartão — é diferente do `id` público, por segurança.
