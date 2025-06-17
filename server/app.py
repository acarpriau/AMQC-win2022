from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import httpx
import time

app = FastAPI()
client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

def get_origin_header_value() -> str:
    return getattr(app.state, "ORIGIN_HEADER_VALUE", "http://127.0.0.1:8081")

# CORS middleware avec un seul origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_origin_header_value()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip middleware pour compresser
# app.add_middleware(GZipMiddleware, minimum_size=500)

async def proxy_request(request: Request, target_url: str):
    body = await request.body()
    
    needed = ["content-type", "accept", "user-agent"]
    headers = {k: v for k, v in request.headers.items() if k.lower() in needed}

    headers["origin"] = get_origin_header_value()
    
    auth = getattr(app.state, "AUTH_HEADER", None)
    if auth:
        headers["Authorization"] = auth

    try:
        resp = await client.request(
            request.method,
            target_url,
            headers=headers,
            content=body,
            params=request.query_params,
            timeout=10.0,
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Proxy error: {exc}")

    excluded_headers = {"content-encoding", "transfer-encoding", "connection"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded_headers}

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=response_headers
    )

@app.api_route("/api/jolokia", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_jolokia_root(request: Request):
    base_url = getattr(app.state, "ACTIVEMQ_URL", "http://localhost:8161")
    target_url = f"{base_url}/api/jolokia"
    return await proxy_request(request, target_url)

@app.api_route("/api/jolokia/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_jolokia_path(request: Request, path: str):
    base_url = getattr(app.state, "ACTIVEMQ_URL", "http://localhost:8161")
    target_url = f"{base_url}/api/jolokia/{path}"
    return await proxy_request(request, target_url)

@app.get("/api/test-vars")
async def test_vars():
    return JSONResponse({
        "ACTIVEMQ_URL": getattr(app.state, "ACTIVEMQ_URL", None),
        "AUTH_HEADER": getattr(app.state, "AUTH_HEADER", None),
        "ORIGIN_HEADER_VALUE": getattr(app.state, "ORIGIN_HEADER_VALUE", None),
        "static_dir_exists": hasattr(app.state, "static_dir"),
    })

@app.get("/api/selftest")
async def selftest():
    base_url = getattr(app.state, "ACTIVEMQ_URL", "http://localhost:8161")
    target_url = f"{base_url}/api/jolokia"

    headers = {"Authorization": getattr(app.state, "AUTH_HEADER", "")}
    
    result = {}

    # Direct Jolokia (pas via proxy)
    start_direct = time.time()
    async with httpx.AsyncClient() as client_test:
        try:
            resp_direct = await client.get(target_url, headers=headers, timeout=10.0)
            duration_direct = time.time() - start_direct
            result["direct_status"] = resp_direct.status_code
            result["direct_duration_ms"] = round(duration_direct * 1000, 2)
        except Exception as e:
            result["direct_error"] = str(e)

    # Via Proxy FastAPI
    host = getattr(app.state, "SERVER_HOST", "127.0.0.1")
    port = getattr(app.state, "SERVER_PORT", 8081)
    proxy_url = f"http://{host}:{port}/api/jolokia"
    
    start_proxy = time.time()
    async with httpx.AsyncClient() as client_test:
        try:
            resp_proxy = await client.get(proxy_url, timeout=10.0)
            start_proxy = time.time()
            duration_proxy = time.time() - start_proxy
            result["proxy_status"] = resp_proxy.status_code
            result["proxy_duration_ms"] = round(duration_proxy * 1000, 2)
        except Exception as e:
            result["proxy_error"] = str(e)

    return result
