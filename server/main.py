import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import app  # Importation de l'application contenant les routes API

# Détection automatique du système et configuration d'ActiveMQ
ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "127.0.0.1") if os.name == "nt" else "localhost"
ACTIVEMQ_PORT = "8161"
ACTIVEMQ_PROTO = "http"
ACTIVEMQ_URL = f"{ACTIVEMQ_PROTO}://{ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}"

# Détection du répertoire statique (racine du projet)
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(base_dir, ".."))  # Remonte à la racine

# Vérifier si le répertoire statique existe
if not os.path.exists(static_dir):
    raise RuntimeError(f"Le répertoire statique '{static_dir}' n'existe pas")

# Ajout des variables globales à FastAPI
app.state.ACTIVEMQ_URL = ACTIVEMQ_URL
app.state.static_dir = static_dir

# Montage du répertoire statique
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
