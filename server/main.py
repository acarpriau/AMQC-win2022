from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import requests
import json
import os

# Base prefix (e.g., /AMQC)
PREFIX = os.getenv("AMQC_PREFIX", "")

# External ActiveMQ host and port
ACTIVEMQ_HOST = os.getenv("ACTIVEMQ_HOST", "localhost")
ACTIVEMQ_PORT = os.getenv("ACTIVEMQ_PORT", "8161")
ACTIVEMQ_PROTO = os.getenv("ACTIVEMQ_PROTO", "http")

# Compute ActiveMQ base URL
ACTIVEMQ_URL = f"{ACTIVEMQ_PROTO}://{ACTIVEMQ_HOST}:{ACTIVEMQ_PORT}"

# App setup
app = FastAPI()

# Dynamically resolve static directory
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")

if not os.path.exists(static_dir):
    raise RuntimeError(f"Static directory '{static_dir}' does not exist")

app.mount(f"{PREFIX}/AMQC", StaticFiles(directory=static_dir), name="static")


# Routes
@app.get(f"{PREFIX}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost")
async def req1(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.get(f"{ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost",
                            headers=headers)
    return response.json()


@app.get(f"{PREFIX}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*")
async def req2(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.get(f"{ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*",
                            headers=headers)
    return response.json()


@app.get(f"{PREFIX}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,connector=clientConnectors,connectorName=*,connectionViewType=clientId,connectionName=*")
async def req3(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.get(f"{ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,connector=clientConnectors,connectorName=*,connectionViewType=clientId,connectionName=*",
                            headers=headers)
    return response.json()


@app.get(f"{PREFIX}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Topic,destinationName=*")
async def req4(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.get(f"{ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Topic,destinationName=*",
                            headers=headers)
    return response.json()


@app.post(f"{PREFIX}/api/jolokia")
async def jolpost(request: Request):
    body = await request.json()
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.post(f"{ACTIVEMQ_URL}/api/jolokia", headers=headers, data=json.dumps(body))
    return response.json()


@app.post(f"{PREFIX}/api/message/{{target}}")
async def jolmessage(request: Request, target, type, Origin, ID):
    body = await request.body()
    url = f"{ACTIVEMQ_URL}/api/message/{target}?type={type}&Origin={Origin}&ID={ID}"
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": ACTIVEMQ_URL}
    response = requests.post(url, headers=headers, data=body.decode("utf-8"))
    return {"result": response.text}
