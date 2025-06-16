from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Fonction pour récupérer origin unique
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

# Proxy pour /api/jolokia (exact)
@app.api_route("/api/jolokia", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_jolokia_root(request: Request):
    base_url = getattr(app.state, "ACTIVEMQ_URL", "http://localhost:8161")
    target_url = f"{base_url}/api/jolokia"

    headers = dict(request.headers)
    headers["origin"] = get_origin_header_value()
    headers["Authorization"] = getattr(app.state, "AUTH_HEADER", "")

    body = await request.body()

    async with httpx.AsyncClient() as client:
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

    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

# Proxy pour /api/jolokia/{path:path}
@app.api_route("/api/jolokia/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def proxy_jolokia_path(request: Request, path: str):
    base_url = getattr(app.state, "ACTIVEMQ_URL", "http://localhost:8161")
    target_url = f"{base_url}/api/jolokia/{path}"

    headers = dict(request.headers)
    headers["origin"] = get_origin_header_value()
    headers["Authorization"] = getattr(app.state, "AUTH_HEADER", "")

    body = await request.body()

    async with httpx.AsyncClient() as client:
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

    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)

# Route pour debug /api/test-vars
@app.get("/api/test-vars")
async def test_vars():
    return JSONResponse({
        "ACTIVEMQ_URL": getattr(app.state, "ACTIVEMQ_URL", None),
        "AUTH_HEADER": getattr(app.state, "AUTH_HEADER", None),
        "ORIGIN_HEADER_VALUE": getattr(app.state, "ORIGIN_HEADER_VALUE", None),
        "static_dir_exists": hasattr(app.state, "static_dir"),
    })
