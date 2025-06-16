import os
import base64
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import app  # FastAPI app

# Config ActiveMQ
ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "localhost")
ACTIVEMQ_PORT = os.getenv("ACTIVEMQ_PORT", "8161")
ACTIVEMQ_BROKER = os.getenv("ACTIVEMQ_BROKER", "localhost")
ACTIVEMQ_USER = os.getenv("ACTIVEMQ_USER", "admin")
ACTIVEMQ_PASS = os.getenv("ACTIVEMQ_PASS", "admin")

ACTIVEMQ_URL = f"http://{ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}"

# Serveur FastAPI HTTP local
AMQC_HOST = "127.0.0.1"
AMQC_PORT = int(os.getenv("AMQC_PORT", "8081"))

# CORS allowed origins (dev direct + prod HTTPS)
AMQC_ORIGINS = [
    "http://127.0.0.1:8081",
    "https://localhost",
]

# Static files path
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(base_dir, "..", "static"))
if not os.path.exists(static_dir):
    raise RuntimeError(f"Static directory '{static_dir}' does not exist")

# Encode Basic Auth header
credentials = f"{ACTIVEMQ_USER}:{ACTIVEMQ_PASS}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()
app.state.AUTH_HEADER = f"Basic {encoded_credentials}"

app.state.ACTIVEMQ_URL = ACTIVEMQ_URL
app.state.ACTIVEMQ_BROKER = ACTIVEMQ_BROKER
app.state.ORIGIN_HEADER_VALUE = AMQC_ORIGINS
app.state.static_dir = static_dir

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

if __name__ == "__main__":
    uvicorn.run(app, host=AMQC_HOST, port=AMQC_PORT)
