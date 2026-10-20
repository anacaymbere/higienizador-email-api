# 📧 Higienizador de E-mails API

> API de alta performance ($O(n)$) desenvolvida com **FastAPI** e **Pydantic** para validação, higienização, desduplicação e correção automática de domínios em listas de e-mails.

---

## 🚀 Funcionalidades

- **Higienização de Strings**: Remove espaços extras no início e fim (`.strip()`) e padroniza para letras minúsculas (`.lower()`)[cite: 2, 3].
- **Correção Inteligente de Domínios**: Identifica e corrige erros de digitação frequentes em provedores populares (ex: `@gmal.com` $\rightarrow$ `@gmail.com`, `@uol.com` $\rightarrow$ `@uol.com.br`)[cite: 1, 2].
- **Validação Sintática**: Valida a estrutura dos e-mails utilizando Expressões Regulares (Regex) otimizadas[cite: 1, 2].
- **Processamento em Lote com Desduplicação $O(n)$**: Processa listas de e-mails em alta velocidade, removendo duplicados de forma eficiente via tabela Hash (`set`).
- **Estatísticas em Tempo Real**: Retorna contadores de e-mails recebidos, únicos e alterados para auditoria rápida.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11+**
* **FastAPI**: Framework web moderno e assíncrono para construção de APIs RESTful[cite: 1, 2].
* **Uvicorn**: Servidor Web ASGI de alta performance[cite: 1, 2].
* **Pydantic**: Validação de schemas e controle de dados[cite: 1, 2].

---

## 📂 Estrutura do Projeto

```text
higienizador-email-api/
│
├── main.py              # Código principal e endpoints do FastAPI
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação técnica do projeto


📦 Dependências (requirements.txt)

fastapi>=0.110.0
uvicorn[standard]>=0.28.0
pydantic>=2.6.0

💻 Como Rodar o Projeto Localmente / Codespaces
1. Clonar o repossitótio

git clone [https://github.com/SEU_USUARIO/higienizador-emails-api.git](https://github.com/SEU_USUARIO/higienizador-emails-api.git)
cd higienizador-emails-api

2. Instalar as dependências
pip install -r requirements.txt

3. Iniciar o servidor
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

4. Acessar a Documentação Interativa (Swagger)
Abra no navegador de sua preferência (ou no Safari do iPad via Codespaces):

Swagger UI: http://localhost:8000/docs ou https://SEU-CODESPACE-8000.app.github.dev/docs

ReDoc: http://localhost:8000/redoc


🔌 Documentação dos Endpoints
1. Healthcheck (GET /)
Verifica a disponibilidade da API para monitoramento na nuvem.
Resposta (200 OK):

{
  "status": "online",
  "servico": "Higienizador de E-mails API"
}


2. Higienizar E-mail Único (POST /v1/higienizar)
Recebe um único e-mail, aplica as regras de limpeza, correção e validação sintática

Requisição (JSON Body):

{
  "email": "   usuario@uol.com   "
}

Resposta (200 OK):

{
  "email_original": "   usuario@uol.com   ",
  "email_higienizado": "usuario@uol.com.br",
  "foi_alterado": true,
  "formato_valido": true
}


3. Higienizar E-mails em Lote (POST /v1/higienizar-lote)
Processa uma lista de e-mails, remove duplicados automaticamente e retorna relatórios e contadores

Requisição (JSON Body):

{
  "emails": [
    "  usuario1@gmal.com  ",
    "CONTATO@UOL.COM",
    "usuario1@gmal.com",
    "teste@outlok.com"
  ]
}

Resposta (200 OK):

{
  "total_recebidos": 4,
  "total_unicos": 3,
  "total_alterados": 3,
  "itens": [
    {
      "email_original": "  usuario1@gmal.com  ",
      "email_higienizado": "usuario1@gmail.com",
      "foi_alterado": true,
      "formato_valido": true
    },
    {
      "email_original": "CONTATO@UOL.COM",
      "email_higienizado": "contato@uol.com.br",
      "foi_alterado": true,
      "formato_valido": true
    },
    {
      "email_original": "teste@outlok.com",
      "email_higienizado": "teste@outlook.com",
      "foi_alterado": true,
      "formato_valido": true
    }
  ]
}


📈 Roadmap de Melhorias Futuras
[ ] Suporte a verificação de registros MX no DNS do domínio.
[ ] Exportação do relatório em formato CSV.
[ ] Integração com sistema de autenticação via API Key.
[ ] Publicação no marketplace do RapidAPI.

📄 Licença
Este projeto está sob a licença MIT - veja o arquivo LICENSE para mais detalhes.