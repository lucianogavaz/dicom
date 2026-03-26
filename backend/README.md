# DICOM Gateway Backend

Backend do MVP do `DICOM Receiver/Gateway` para Windows.

## Componentes

- `API FastAPI`
  Exibe status, fila e destinos configurados.
- `DICOM Receiver`
  Atua como `Storage SCP` para recepcao de imagens XA.
- `Sender`
  Atua como `Storage SCU` para envio ao PACS.
- `Worker`
  Faz polling da fila e tenta o encaminhamento.

## Estrutura

- [app\main.py](C:\dicom_gateway\backend\app\main.py)
  Entrada da API.
- [app\run_receiver.py](C:\dicom_gateway\backend\app\run_receiver.py)
  Entrada do listener DICOM.
- [app\run_worker.py](C:\dicom_gateway\backend\app\run_worker.py)
  Entrada do worker.
- [app\api\routes](C:\dicom_gateway\backend\app\api\routes)
  Endpoints HTTP.
- [app\db\models.py](C:\dicom_gateway\backend\app\db\models.py)
  Modelos do banco.
- [app\services](C:\dicom_gateway\backend\app\services)
  Regras de negocio e integracao DICOM.

## Endpoints Atuais

- `GET /health`
- `GET /queue`
- `GET /queue/{id}`
- `POST /queue/{id}/resend`
- `GET /endpoints`
- `POST /endpoints`
- `POST /endpoints/{id}/test`

## Configuracao

Use [backend\.env](C:\dicom_gateway\backend\.env) como configuracao inicial.

Campos principais:
- `DATABASE_URL`
- `LOCAL_AE_TITLE`
- `LOCAL_DICOM_PORT`
- `LOCAL_STORAGE_PATH`
- `DEFAULT_REMOTE_AE_TITLE`
- `DEFAULT_REMOTE_HOST`
- `DEFAULT_REMOTE_PORT`
- `WORKER_POLL_SECONDS`
- `MAX_RETRIES`

## Setup

1. Revise [backend\.env](C:\dicom_gateway\backend\.env).
2. Crie o banco com [create_postgres_db.bat](C:\dicom_gateway\scripts\create_postgres_db.bat), se necessario.
3. Rode [setup_backend.bat](C:\dicom_gateway\scripts\setup_backend.bat).
4. Valide com [validate_setup.bat](C:\dicom_gateway\validate_setup.bat).

## Execucao Manual

- API:
  `C:\dicom_gateway\scripts\run_api.bat`
- Receiver:
  `C:\dicom_gateway\scripts\run_receiver.bat`
- Worker:
  `C:\dicom_gateway\scripts\run_worker.bat`

## Observacoes

- O projeto agora ja vem preparado para `PostgreSQL` local.
- Se voce ainda quiser um bootstrap mais simples, pode trocar temporariamente o `DATABASE_URL` para `SQLite`.
- O sender atual envia para um destino padrao configurado no `.env`.
- O teste de conectividade do endpoint ainda esta em modo `stub`.

## Proximos Passos

1. Migrar o banco padrao para PostgreSQL.
2. Implementar `C-ECHO` real no teste de endpoint.
3. Criar frontend web.
4. Adicionar autenticacao e trilha de auditoria mais completa.
