# Database Guide

## Objetivo

O banco guarda metadados operacionais, status de fila e configuracoes de destino. Os arquivos DICOM devem permanecer no filesystem, nao dentro do banco.

## Banco Atual

O projeto agora esta configurado para `PostgreSQL` local via:

- [config.py](C:\dicom_gateway\backend\app\core\config.py)
- [.env](C:\dicom_gateway\backend\.env)

Valor padrao:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/dicom_gateway
```

Criacao inicial do banco:

- [create_postgres_db.sql](C:\dicom_gateway\scripts\create_postgres_db.sql)
- [create_postgres_db.bat](C:\dicom_gateway\scripts\create_postgres_db.bat)

## Tabelas Atuais

### `dicom_endpoints`

Usada para destinos PACS configurados.

Campos principais:
- `id`
- `name`
- `ae_title`
- `host`
- `port`
- `enabled`
- `is_default`
- `created_at`

### `dicom_instance_queue`

Usada para controlar a fila de envio.

Campos principais:
- `id`
- `study_instance_uid`
- `series_instance_uid`
- `sop_instance_uid`
- `sop_class_uid`
- `transfer_syntax_uid`
- `modality`
- `patient_id`
- `source_ae_title`
- `source_ip`
- `destination_endpoint_id`
- `destination_ae_title`
- `file_path`
- `status`
- `retry_count`
- `max_retries`
- `last_error`
- `received_at`
- `last_attempt_at`
- `sent_at`

## Status de Fila

- `PENDING_SEND`
- `SENDING`
- `SENT`
- `RETRY_PENDING`
- `FAILED`

## Recomendacao Para Evolucao

Exemplo de ajuste:

```env
DATABASE_URL=postgresql+psycopg://postgres:senha@localhost:5432/dicom_gateway
```

## Motivos Para PostgreSQL

- maior confiabilidade operacional
- melhor concorrencia
- facilidade de backup
- melhor suporte a auditoria e crescimento

## Observacao Atual

As tabelas sao criadas automaticamente via:

- [main.py](C:\dicom_gateway\backend\app\main.py)
- [run_receiver.py](C:\dicom_gateway\backend\app\run_receiver.py)
- [run_worker.py](C:\dicom_gateway\backend\app\run_worker.py)

No futuro, o ideal e substituir isso por `Alembic` com migracoes versionadas.
