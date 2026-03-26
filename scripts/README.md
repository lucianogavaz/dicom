# Scripts

Esta pasta concentra os scripts `.bat` para preparar, validar, executar e instalar o projeto no Windows.

## Scripts de Ambiente

- [setup_backend.bat](C:\dicom_gateway\scripts\setup_backend.bat)
  Cria `.venv`, instala dependencias Python e gera `requirements.txt`.
- [..\\check_env.bat](C:\dicom_gateway\check_env.bat)
  Verifica ferramentas e pastas principais.
- [..\\validate_setup.bat](C:\dicom_gateway\validate_setup.bat)
  Valida instalacoes e pacotes Python.

## Scripts de Execucao

- [run_api.bat](C:\dicom_gateway\scripts\run_api.bat)
  Inicia a API FastAPI.
- [run_receiver.bat](C:\dicom_gateway\scripts\run_receiver.bat)
  Inicia o receiver DICOM.
- [run_worker.bat](C:\dicom_gateway\scripts\run_worker.bat)
  Inicia o worker de envio.

## Scripts de Servico Windows

- [install_api_service.bat](C:\dicom_gateway\scripts\install_api_service.bat)
- [install_receiver_service.bat](C:\dicom_gateway\scripts\install_receiver_service.bat)
- [install_worker_service.bat](C:\dicom_gateway\scripts\install_worker_service.bat)
- [start_services.bat](C:\dicom_gateway\scripts\start_services.bat)
- [stop_services.bat](C:\dicom_gateway\scripts\stop_services.bat)
- [remove_services.bat](C:\dicom_gateway\scripts\remove_services.bat)

## Ordem Recomendada

1. Rode [..\\check_env.bat](C:\dicom_gateway\check_env.bat).
2. Instale as dependencias faltantes.
3. Rode [setup_backend.bat](C:\dicom_gateway\scripts\setup_backend.bat).
4. Copie `.env.example` para `.env`.
5. Rode os scripts de execucao manual.
6. Depois instale como servico com `NSSM`.
