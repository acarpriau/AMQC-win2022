from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import httpx

app = FastAPI()

# CORS middleware for both dev and prod origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8081",
        "https://localhost"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to respect X-Forwarded-Prefix header (for Nginx /amqc prefix)
class RootPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if "x-forwarded-prefix" in request.headers:
            request.scope["root_path"] = request.headers["x-forwarded-prefix"]
        response = await call_next(request)
        return response

app.add_middleware(RootPathMiddleware)

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER

    if request.method == "OPTIONS":
        # CORS preflight response
        response_headers = {
            "Access-Control-Allow-Origin": ", ".join(app.state.ORIGIN_HEADER_VALUE),
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Max-Age": "3600",
        }
        return Response(status_code=204, headers=response_headers)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    # Inject CORS headers for client UI
    response_headers["Access-Control-Allow-Origin"] = ", ".join(app.state.ORIGIN_HEADER_VALUE)
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)


@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_message(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": ", ".join(app.state.ORIGIN_HEADER_VALUE),
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Authorization,Content-Type",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
            "Access-Control-Max-Age": "3600",
        }
        return Response(status_code=204, headers=response_headers)

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    response_headers = dict(resp.headers)
    response_headers["Access-Control-Allow-Origin"] = ", ".join(app.state.ORIGIN_HEADER_VALUE)
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
