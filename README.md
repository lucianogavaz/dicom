# DICOM Gateway

Projeto base de um `DICOM Receiver/Gateway` para hemodinamica, com foco em recepcao de imagens `XA` e envio posterior para um `PACS`.

## Objetivo

O sistema recebe imagens DICOM enviadas por um equipamento XA, valida o dataset, grava temporariamente os arquivos em disco, registra o item em fila e tenta encaminha-lo ao PACS de destino.

## Arquitetura

- `backend`
  API, receiver DICOM, sender e worker.
- `frontend`
  Espaco reservado para a interface web.
- `storage`
  Buffer local dos arquivos DICOM.
- `scripts`
  Automacao de setup, execucao e instalacao como servico Windows.
- `docs`
  Documentacao operacional e tecnica.

## Fluxo

1. O equipamento XA envia um `C-STORE` para o receiver.
2. O receiver valida o objeto DICOM.
3. O arquivo e salvo em `storage\incoming`.
4. Um registro e criado na fila do banco.
5. O worker tenta enviar o arquivo para o PACS.
6. O status e atualizado para `SENT`, `RETRY_PENDING` ou `FAILED`.

## Estrutura Atual

- [backend](C:\dicom_gateway\backend)
- [frontend](C:\dicom_gateway\frontend)
- [storage](C:\dicom_gateway\storage)
- [scripts](C:\dicom_gateway\scripts)
- [docs](C:\dicom_gateway\docs)

## Primeiro Uso

1. Instale `Python`, `Git`, `PostgreSQL` e `NSSM`.
2. Rode [check_env.bat](C:\dicom_gateway\check_env.bat).
3. Rode [validate_setup.bat](C:\dicom_gateway\validate_setup.bat) apos as instalacoes.
4. Rode [setup_backend.bat](C:\dicom_gateway\scripts\setup_backend.bat).
5. Revise [backend\.env](C:\dicom_gateway\backend\.env).
6. Crie o banco com [create_postgres_db.bat](C:\dicom_gateway\scripts\create_postgres_db.bat).
7. Inicie a API, o receiver e o worker.

## Documentacao

- [Backend README](C:\dicom_gateway\backend\README.md)
- [Frontend README](C:\dicom_gateway\frontend\README.md)
- [Scripts README](C:\dicom_gateway\scripts\README.md)
- [Docs README](C:\dicom_gateway\docs\README.md)
- [Database Guide](C:\dicom_gateway\docs\DATABASE.md)
- [Windows Operations Guide](C:\dicom_gateway\docs\WINDOWS_SETUP.md)
