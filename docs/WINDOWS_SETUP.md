# Windows Setup And Operations

## Requisitos

- `Windows 10/11` ou `Windows Server`
- `Python 3.12`
- `Git`
- `PostgreSQL`
- `Node.js`
- `NSSM`

## Validacao Inicial

Rode:

```bat
C:\dicom_gateway\check_env.bat
```

Depois da instalacao das dependencias, rode:

```bat
C:\dicom_gateway\validate_setup.bat
```

## Setup Do Backend

1. Rode:

```bat
C:\dicom_gateway\scripts\setup_backend.bat
```

2. Crie o banco:

```bat
C:\dicom_gateway\scripts\create_postgres_db.bat
```

3. Revise:

- [backend\.env](C:\dicom_gateway\backend\.env)

4. Ajuste os valores de:
- `DATABASE_URL`
- `LOCAL_AE_TITLE`
- `LOCAL_DICOM_PORT`
- `LOCAL_STORAGE_PATH`
- `DEFAULT_REMOTE_AE_TITLE`
- `DEFAULT_REMOTE_HOST`
- `DEFAULT_REMOTE_PORT`

## Execucao Manual

Em janelas separadas:

```bat
C:\dicom_gateway\scripts\run_api.bat
```

```bat
C:\dicom_gateway\scripts\run_receiver.bat
```

```bat
C:\dicom_gateway\scripts\run_worker.bat
```

## Execucao Como Servico

Depois de instalar `NSSM`:

```bat
C:\dicom_gateway\scripts\install_api_service.bat
C:\dicom_gateway\scripts\install_receiver_service.bat
C:\dicom_gateway\scripts\install_worker_service.bat
```

Para iniciar:

```bat
C:\dicom_gateway\scripts\start_services.bat
```

Para parar:

```bat
C:\dicom_gateway\scripts\stop_services.bat
```

Para remover:

```bat
C:\dicom_gateway\scripts\remove_services.bat
```

## Logs

Os logs ficam em:

- [logs](C:\dicom_gateway\logs)

Arquivos principais esperados:
- `app.log`
- `api-service.out.log`
- `api-service.err.log`
- `receiver-service.out.log`
- `receiver-service.err.log`
- `worker-service.out.log`
- `worker-service.err.log`

## Firewall

Libere pelo menos:
- porta `11112` para DICOM
- porta `8000` para a API
- porta do `PostgreSQL`, se estiver remoto
- porta do PACS de destino

## Observacoes

- Para testes locais, o banco padrao atual e `SQLite`.
- Para operacao real, use `PostgreSQL`.
- O frontend ainda nao foi implementado.
- O sender atual trabalha com um destino padrao configurado no `.env`.
