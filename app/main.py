from fastapi import FastAPI
from app.routers import produtos, encomendas

app = FastAPI(
    title="API de Encomendas",
    description="API REST para cadastro e gerenciamento de produtos e encomendas",
    version="0.1.0",
)

app.include_router(produtos.router)
app.include_router(encomendas.router)


@app.get("/")
def root():
    return {"message": "API de Encomendas funcionando!"}
