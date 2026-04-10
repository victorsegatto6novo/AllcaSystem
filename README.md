# Sistema de Monitoramento de Alarmes (Sigma-like)

Projeto base em Python para central de monitoramento com:

- Cadastro de clientes
- Painel web com colunas (kanban) para atendimento de eventos
- API para ingestão e atualização de eventos
- Estruturas de integração com receptor IP Intelbras (Firebird `receptorip.fdb`) e receptora CAF CM4000 na `COM3`

## Stack

- FastAPI + Jinja2
- SQLAlchemy + SQLite (local)
- Front-end HTML/CSS/JS com drag-and-drop

## Executar

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse:
- `http://localhost:8000/` (painel em colunas)
- `http://localhost:8000/clients` (cadastro de clientes)

## Observações importantes de integração real

1. **Firebird (receptorip.fdb)**
   - Arquivo: `app/services/firebird_reader.py`
   - Ajuste `query` para o schema real do seu banco receptor IP Intelbras.

2. **CAF CM4000 em COM3**
   - Arquivo: `app/services/serial_receiver.py`
   - Ajuste baudrate, framing e parser da linha conforme seu protocolo.

3. **Produção**
   - Substituir SQLite por PostgreSQL.
   - Rodar workers de ingestão contínua para Firebird/serial.
   - Adicionar autenticação, auditoria e SLA de atendimento.
