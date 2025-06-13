from fastapi import FastAPI, Request
import requests
import json

# Création de l'application FastAPI
app = FastAPI()

# Les variables de configuration (URL ActiveMQ, répertoire statique) sont gérées par `main.py`

# Routes API Jolokia
@app.get("/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost")
async def req1(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": app.state.ACTIVEMQ_URL}
    response = requests.get(f"{app.state.ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost", headers=headers)
    return response.json()

@app.get("/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*")
async def req2(request: Request):
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": app.state.ACTIVEMQ_URL}
    response = requests.get(f"{app.state.ACTIVEMQ_URL}/api/jolokia/read/org.apache.activemq:type=Broker,brokerName=localhost,destinationType=Queue,destinationName=*", headers=headers)
    return response.json()

@app.post("/api/jolokia")
async def jolpost(request: Request):
    body = await request.json()
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": app.state.ACTIVEMQ_URL}
    response = requests.post(f"{app.state.ACTIVEMQ_URL}/api/jolokia", headers=headers, data=json.dumps(body))
    return response.json()

@app.post("/api/message/{target}")
async def jolmessage(request: Request, target, type, Origin, ID):
    body = await request.body()
    url = f"{app.state.ACTIVEMQ_URL}/api/message/{target}?type={type}&Origin={Origin}&ID={ID}"
    auth = request.headers.get("authorization")
    headers = {"authorization": auth, "referer": app.state.ACTIVEMQ_URL}
    response = requests.post(url, headers=headers, data=body.decode("utf-8"))
    return {"result": response.text}
