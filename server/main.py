import os
import base64
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import app  # Import de l'app FastAPI

# Config ActiveMQ
ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "localhost")
ACTIVEMQ_PORT = os.getenv("ACTIVEMQ_PORT", "8161")
ACTIVEMQ_BROKER = os.getenv("ACTIVEMQ_BROKER", "localhost")
ACTIVEMQ_USER = os.getenv("ACTIVEMQ_USER", "admin")
ACTIVEMQ_PASS = os.getenv("ACTIVEMQ_PASS", "admin")

ACTIVEMQ_URL = f"http://{ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}"

# Serveur FastAPI
AMQC_HOST = os.getenv("AMQC_HOST", "127.0.0.1")
AMQC_PORT = int(os.getenv("AMQC_PORT", "8081"))

# Un seul origin autorisé ici
# Modifie cette valeur selon ton besoin exact (ex: "https://localhost" ou "http://127.0.0.1:8081")
AMQC_ORIGIN = "http://127.0.0.1:8081"

# Répertoire statique (le dossier 'static' au-dessus de ce script)
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(base_dir, "..", "static"))
if not os.path.exists(static_dir):
    raise RuntimeError(f"Static directory '{static_dir}' does not exist")

# Préparer l’en-tête Basic Auth encodé
credentials = f"{ACTIVEMQ_USER}:{ACTIVEMQ_PASS}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
app.state.AUTH_HEADER = f"Basic {encoded_credentials}"

app.state.ACTIVEMQ_URL = ACTIVEMQ_URL
app.state.ACTIVEMQ_BROKER = ACTIVEMQ_BROKER
app.state.ORIGIN_HEADER_VALUE = AMQC_ORIGIN  # string, pas liste
app.state.static_dir = static_dir

app.state.SERVER_HOST = AMQC_HOST
app.state.SERVER_PORT = AMQC_PORT

# Lis le préfixe depuis une variable d'environnement, par défaut vide
prefix = os.getenv("STATIC_PREFIX", "")

# Ajoute le / devant si nécessaire
if prefix and not prefix.startswith("/"):
    prefix = "/" + prefix
    
# Monter les fichiers statiques pour servir le front
app.mount(prefix, StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host=AMQC_HOST, port=AMQC_PORT)
