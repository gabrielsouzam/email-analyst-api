# 📧 Email Analyst API

API REST para classificação inteligente de emails utilizando Google Gemini AI.

## 🚀 Tecnologias

- **FastAPI** - Framework web moderno e rápido
- **Python 3.11+** - Linguagem de programação
- **Google Gemini AI** - Modelo de linguagem para classificação
- **Pydantic** - Validação de dados
- **PyPDF2** - Processamento de arquivos PDF
- **Uvicorn** - Servidor ASGI

## 📋 Pré-requisitos

- Docker instaldo na máquina
- Chave de API do Google Gemini ([obtenha aqui](https://makersuite.google.com/app/apikey))

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/gabrielsouzam/email-analyst-api
cd email-analyst-api
```

## ⚙️ Configuração

Crie um arquivo `.env` no diretório raiz com sua chave da API do Google:

```
GEMINI_API_KEY=sua_chave_api_aqui
GOOGLE_API_MODEL=gemini-2.0-flash
ENVIRONMENT=development
```

**Nota:** Obtenha sua chave gratuita em [Google AI Studio](https://makersuite.google.com/app/apikey)

## Como rodar o projeto

### Executando com Docker

1. Construa a imagem Docker:
```bash
docker build -t email-analyst-api .
```

2. Execute o container:
```bash
docker run --env-file=.env -p 5000:5000 email-analyst-api
```

### Executando localmente

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

Acesse: `http://localhost:5000`

## Uso

- Envie uma requisição POST para `/email/analysis` com o texto do email.
- Envie uma requisição POST para `/email/analysis/file` com arquivo .txt ou .pdf.

### Exemplo com texto:

```bash
POST /email/analysis
Content-Type: application/json

{
  "content": "Preciso do relatório de vendas urgente para hoje!"
}
```

### Exemplo com arquivo:

```bash
POST /email/analysis/file
Content-Type: multipart/form-data

file: email.txt
```

### Resposta:

```json
{
  "category": "productive",
  "response": "Recebi sua solicitação do relatório de vendas. Vou priorizar e enviar até o final do dia de hoje. Caso precise de alguma informação específica, por favor me avise."
}
```

## Documentação da API

Após executar a aplicação, acesse:
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## 🎯 Funcionalidades

- ✅ Classificação de emails (Produtivo/Improdutivo)
- ✅ Geração automática de respostas
- ✅ Processamento de arquivos .txt e .pdf

## 👨‍💻 Autor

Desenvolvido por Gabriel Mendes 💙!