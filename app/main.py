from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError
from app.presentation.api.auth_router import router as auth_router
from app.presentation.api.atleta_router import router as atleta_router
from app.presentation.api.elenco_router import router as elenco_router
from app.presentation.api.jogo_router import router as jogo_router

app = FastAPI(
    title="Sistema de Gerenciamento Esportivo",
    description="API para gerenciamento de usuários, atletas, elencos e jogos.",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(atleta_router)
app.include_router(elenco_router)
app.include_router(jogo_router)


@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


@app.get("/", tags=["Início"])
def raiz():
    return {"mensagem": "Bem-vindo à API do Sistema Esportivo!"}


@app.get("/health", tags=["Início"])
def health():
    return {"status": "ok"}