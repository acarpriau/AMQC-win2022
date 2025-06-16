from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia(request: Request, full_path: str):
    if request.method == "OPTIONS":
        # Réponse CORS preflight
        headers = {
            "Access-Control-Allow-Origin": "http://127.0.0.1:8081",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH"
        }
        return Response(content="", status_code=204, headers=headers)

    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    headers["authorization"] = app.state.AUTH_HEADER
    headers["referer"] = app.state.ACTIVEMQ_URL

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8081"
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)

@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_message(request: Request, full_path: str):
    if request.method == "OPTIONS":
        # Réponse CORS preflight
        headers = {
            "Access-Control-Allow-Origin": "http://127.0.0.1:8081",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH"
        }
        return Response(content="", status_code=204, headers=headers)

    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"
    headers = dict(request.headers)
    headers.pop("host", None)
    headers["authorization"] = app.state.AUTH_HEADER
    headers["referer"] = app.state.ACTIVEMQ_URL

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = "http://127.0.0.1:8081"
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
