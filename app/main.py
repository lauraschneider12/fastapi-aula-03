
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions import ApplicationError

# Routers
from app.presentation.api.auth_router import router as auth_router
from app.presentation.api.atleta_router import router as atleta_router
from app.presentation.api.elenco_router import router as elenco_router
from app.presentation.api.jogo_router import router as jogo_router
from app.presentation.api.gol_router import router as gol_router
from app.presentation.api.cartao_router import router as cartao_router
from app.presentation.api.public_router import router as public_router
from app.presentation.api.treino_router import router as treino_router
from app.presentation.api.presenca_router import router as presenca_router
from app.presentation.api.aviso_router import router as aviso_router
from app.presentation.api.atleta_area_router import router as atleta_area_router


app = FastAPI(
    title="Sistema de Gerenciamento Esportivo",
    description="API para gerenciamento de usuários, atletas, elencos, jogos, gols e cartões.",
    version="1.0.0",
)


# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registro dos routers
app.include_router(auth_router)
app.include_router(atleta_router)
app.include_router(elenco_router)
app.include_router(jogo_router)
app.include_router(gol_router)
app.include_router(cartao_router)
app.include_router(public_router)
app.include_router(treino_router)
app.include_router(presenca_router)
app.include_router(aviso_router)
app.include_router(atleta_area_router)
# Tratamento de erros da aplicação
@app.exception_handler(ApplicationError)
async def application_error_handler(
    request: Request,
    exc: ApplicationError,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


# Rota inicial
@app.get("/", tags=["Início"])
def raiz():
    return {"mensagem": "Bem-vindo à API do Sistema Esportivo!"}


# Verificação da API
@app.get("/health", tags=["Início"])
def health():
    return {"status": "ok"}
