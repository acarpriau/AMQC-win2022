from fastapi import FastAPI, Request, Response
import httpx
from httpx import BasicAuth

app = FastAPI()

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL

    # Ajout Basic Auth
    auth = BasicAuth(app.state.ACTIVEMQ_USER, app.state.ACTIVEMQ_PASS)

    async with httpx.AsyncClient(auth=auth) as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    # Nettoyer certains headers sensibles avant de renvoyer la réponse (optionnel)
    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)


@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_message(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL

    auth = BasicAuth(app.state.ACTIVEMQ_USER, app.state.ACTIVEMQ_PASS)

    async with httpx.AsyncClient(auth=auth) as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    excluded_headers = ["content-encoding", "transfer-encoding", "connection"]
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
