from fastapi import FastAPI, Request, Response
import httpx
import base64

app = FastAPI()

# Construire l'entête Authorization Basic à partir des infos stockées dans app.state
def get_basic_auth_header():
    user = app.state.ACTIVEMQ_USER
    passwd = app.state.ACTIVEMQ_PASS
    user_pass = f"{user}:{passwd}"
    encoded = base64.b64encode(user_pass.encode()).decode()
    return f"Basic {encoded}"

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = get_basic_auth_header()

    async with httpx.AsyncClient() as client:
        if request.method == "GET" or request.method == "OPTIONS":
            resp = await client.request(request.method, target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8081"
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)

@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_message(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = get_basic_auth_header()

    async with httpx.AsyncClient() as client:
        if request.method == "GET" or request.method == "OPTIONS":
            resp = await client.request(request.method, target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8081"
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
