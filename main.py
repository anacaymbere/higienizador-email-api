from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import re

# 1. Inicializa a aplicação FastAPI
app = FastAPI(
    title="Higienizador de E-mails API",
    description="API de alta performance para validação, higienização, desduplicação e correção de domínios em e-mails.",
    version="1.1.0"
)

# 2. Dicionário de mapeamento para correções de domínios comuns
CORRECOES_DOMINIO = {
    "@gmal.com": "@gmail.com",
    "@gmeil.com": "@gmail.com",
    "@gamil.com": "@gmail.com",
    "@hotmial.com": "@hotmail.com",
    "@hotmle.com": "@hotmail.com",
    "@outlok.com": "@outlook.com",
    "@uol.com": "@uol.com.br",
    "@yahoo.com.b": "@yahoo.com.br"
}

# Expressão regular para validação de formato sintático de e-mail
REGEX_EMAIL_VALIDO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


# 3. Modelos de entrada e saída (Schemas Pydantic)
class EmailIndividualRequest(BaseModel):
    email: str = Field(..., example="  usuario@uol.com  ", description="E-mail a ser higienizado")


class EmailLoteRequest(BaseModel):
    emails: list[str] = Field(
        ..., 
        example=["  usuario1@gmal.com  ", "CONTATO@UOL.COM", "usuario1@gmal.com"], 
        description="Lista de e-mails para higienização e desduplicação em lote"
    )


class EmailResponse(BaseModel):
    email_original: str
    email_higienizado: str
    foi_alterado: bool
    formato_valido: bool


class LoteResponse(BaseModel):
    total_recebidos: int
    total_unicos: int
    total_alterados: int
    itens: list[EmailResponse]


# 4. Função core de processamento individual
def processar_email_individual(email_cru: str) -> EmailResponse:
    if not email_cru:
        return EmailResponse(
            email_original="",
            email_higienizado="",
            foi_alterado=False,
            formato_valido=False
        )

    # 1. Remove espaços e converte para minúsculas
    email_limpo = email_cru.strip().lower()

    # 2. Guarda a versão limpa ANTES das substituições para comparar no final
    email_base_para_comparacao = email_limpo

    # 3. Substitui vírgula por ponto no e-mail inteiro
    if "," in email_limpo:
        email_limpo = email_limpo.replace(",", ".")

    email_resultado = email_limpo

    # 4. Aplica a correção de domínio
    for erro, correcao in CORRECOES_DOMINIO.items():
        if email_limpo.endswith(erro):
            email_resultado = email_limpo.rsplit(erro, 1)[0] + correcao
            break

    # 5. Validação Regex
    valido = bool(REGEX_EMAIL_VALIDO.match(email_resultado))

    return EmailResponse(
        email_original=email_cru,
        email_higienizado=email_resultado,
        foi_alterado=(email_base_para_comparacao != email_resultado or email_cru != email_resultado),
        formato_valido=valido
    )
    

# 5. Endpoints da API

@app.get("/", tags=["Healthcheck"])
def healthcheck():
    """Rota para verificar se a API está online."""
    return {"status": "online", "servico": "Higienizador de E-mails API"}


@app.post("/v1/higienizar", response_model=EmailResponse, tags=["Higienização"])
def higienizar_email_unico(payload: EmailIndividualRequest):
    """
    Recebe um e-mail individual, limpa espaços, converte para minúsculas, 
    corrige domínios incorretos e valida o formato.
    """
    return processar_email_individual(payload.email)


@app.post("/v1/higienizar-lote", response_model=LoteResponse, tags=["Higienização"])
def higienizar_emails_em_lote(payload: EmailLoteRequest):
    """
    Processa uma lista completa de e-mails mantendo alta performance:
    - Garante remoção de itens duplicados.
    - Processa e corrige cada registro individualmente.
    - Retorna contadores e estatísticas do lote.
    """
    if not payload.emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A lista de e-mails fornecida não pode estar vazia."
        )

    # Remoção de duplicados mantendo complexidade eficiente O(n)
    emails_unicos = set(payload.emails)
    
    resultados: list[EmailResponse] = []
    total_alterados = 0

    for email in emails_unicos:
        res = processar_email_individual(email)
        if res.foi_alterado:
            total_alterados += 1
        resultados.append(res)

    return LoteResponse(
        total_recebidos=len(payload.emails),
        total_unicos=len(emails_unicos),
        total_alterados=total_alterados,
        itens=resultados
    )