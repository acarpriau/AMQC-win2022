from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

origin_header = getattr(app.state, "ORIGIN_HEADER_VALUE", "http://localhost:8081")

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL
    headers["authorization"] = app.state.AUTH_HEADER
    headers["origin"] = origin_header

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": origin_header,
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
    response_headers["Access-Control-Allow-Origin"] = origin_header
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
    headers["origin"] = origin_header

    if request.method == "OPTIONS":
        response_headers = {
            "Access-Control-Allow-Origin": origin_header,
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
    response_headers["Access-Control-Allow-Origin"] = origin_header
    response_headers["Access-Control-Allow-Credentials"] = "true"
    response_headers["Access-Control-Allow-Headers"] = "Authorization,Content-Type"
    response_headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS,PATCH"

    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers)
