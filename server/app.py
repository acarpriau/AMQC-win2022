from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

@app.get("/api/test-vars")
async def test_vars():
    return {
        "ACTIVEMQ_URL": getattr(app.state, "ACTIVEMQ_URL", None),
        "AUTH_HEADER": getattr(app.state, "AUTH_HEADER", None),
        "ORIGIN_HEADER_VALUE": getattr(app.state, "ORIGIN_HEADER_VALUE", None),
        "static_dir_exists": os.path.exists(getattr(app.state, "static_dir", ""))
    }

# Proxy pour /api/jolokia exactement (pas de suffixe)
@app.api_route("/api/jolokia", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia_root(request: Request):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER
    headers["origin"] = app.state.ORIGIN_HEADER_VALUE

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": app.state.ORIGIN_HEADER_VALUE,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Max-Age": "3600"
        }
        return Response(status_code=204, headers=response_headers)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = app.state.ORIGIN_HEADER_VALUE
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)

# Proxy pour /api/jolokia/ plus chemin dynamique
@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER
    headers["origin"] = app.state.ORIGIN_HEADER_VALUE

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": app.state.ORIGIN_HEADER_VALUE,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Max-Age": "3600"
        }
        return Response(status_code=204, headers=response_headers)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = app.state.ORIGIN_HEADER_VALUE
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)


# Proxy pour /api/message/ avec chemin dynamique
@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_message(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER
    headers["origin"] = app.state.ORIGIN_HEADER_VALUE

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": app.state.ORIGIN_HEADER_VALUE,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Max-Age": "3600"
        }
        return Response(status_code=204, headers=response_headers)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = app.state.ORIGIN_HEADER_VALUE
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
