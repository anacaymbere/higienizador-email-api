
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(
title = "Minha API Python",
description = "API inicial para desenvolvimento e testes",
version = "1.0.0"
)

class Item(BaseModel):
    nome: str
    descricao: str | None = None
    

@app.get("/")
def home():
    return{"status":"API online", "mensagem": "Ambiente configurado com successo!"} 

@app.post("/items")
def cria_item(item:Item):
    return{"status": "criado", "dados": item}
