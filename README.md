# DICOM Web App (Receiver ➜ DICOM Store)

Aplicação em **Python** com interface web (FastAPI) que:

1. Recebe exames DICOM via **C-STORE** (SCP), conforme padrão DICOM/NEMA.
2. Encaminha imediatamente o objeto recebido para um PACS remoto (**DICOM Store**, como SCU).
3. Expõe endpoints web para monitoramento.

## Arquitetura

- **Entrada DICOM**: `pynetdicom` rodando como SCP (`DICOM_LISTEN_AE_TITLE` / `DICOM_LISTEN_PORT`)
- **Saída DICOM**: associação com PACS remoto e envio via `send_c_store`
- **Web API**: FastAPI com endpoints de saúde e status

## Requisitos

- Python 3.11+

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração (variáveis de ambiente)

| Variável | Default | Descrição |
|---|---:|---|
| `DICOM_LISTEN_AE_TITLE` | `DICOMRCV` | AE Title local (SCP) |
| `DICOM_LISTEN_PORT` | `11112` | Porta local para receber C-STORE |
| `PACS_AE_TITLE` | `DICOMSTORE` | AE Title do PACS destino |
| `PACS_HOST` | `127.0.0.1` | Host do PACS destino |
| `PACS_PORT` | `104` | Porta do PACS destino |

Exemplo:

```bash
export DICOM_LISTEN_AE_TITLE=DICOMRCV
export DICOM_LISTEN_PORT=11112
export PACS_AE_TITLE=DCM4CHEE
export PACS_HOST=10.10.10.50
export PACS_PORT=11113
```

## Executar

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Endpoints web

- `GET /health` → status básico da API
- `GET /status` → configuração ativa, estatísticas e últimos erros

## Teste rápido do receiver

Com o aplicativo rodando e um arquivo `sample.dcm`:

```bash
storescu 127.0.0.1 11112 sample.dcm -aec DICOMRCV
```

Após receber, a aplicação tentará encaminhar o exame para o PACS configurado (`PACS_HOST:PACS_PORT`).

## Observações de conformidade DICOM/NEMA

- A aplicação negocia múltiplas Storage SOP Classes para receber e enviar exames.
- O comportamento de aceitação/rejeição final depende também das políticas do PACS destino (AE Title, IP, portas e SOP Classes habilitadas).
- Em produção, recomenda-se executar atrás de VPN/rede segura e adicionar TLS DICOM quando disponível no seu PACS.
