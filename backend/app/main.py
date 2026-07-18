from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.mqtt_client import start_mqtt

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando o servidor FastAPI...")
    start_mqtt()
    yield
    print("Encerrando o servidor FastAPI...")

app = FastAPI(
    title="Controle de Produção P2S BambuLab API",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "API do Controle de Produção P2S BambuLab funcionando!"}