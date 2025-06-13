import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import app  # ton app FastAPI avec routes API

# Config ActiveMQ
ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "127.0.0.1") if os.name == "nt" else "localhost"
ACTIVEMQ_PORT = "8161"
ACTIVEMQ_PROTO = "http"
ACTIVEMQ_URL = f"{ACTIVEMQ_PROTO}://{ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}"

# Host d'écoute
AMQC_HOST = "0.0.0.0"

# Port d'écoute récupéré depuis variable d'env (par défaut 8081)
AMQC_PORT = int(os.getenv("AMQC_PORT", "8081"))

# Répertoire statique
base_dir = os.path.dirname(os.path.abspath(__file__))  # dossier server
static_dir = os.path.abspath(os.path.join(base_dir, "..", "static"))

if not os.path.exists(static_dir):
    raise RuntimeError(f"Le répertoire statique '{static_dir}' n'existe pas")

app.state.ACTIVEMQ_URL = ACTIVEMQ_URL
app.state.static_dir = static_dir

#app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)

if __name__ == "__main__":
    uvicorn.run(app, host=AMQC_HOST, port=AMQC_PORT)
