from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

@app.api_route("/api/jolokia/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_jolokia(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/jolokia/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)


@app.api_route("/api/message/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_message(request: Request, full_path: str):
    target_url = f"{app.state.ACTIVEMQ_URL}/api/message/{full_path}"

    headers = dict(request.headers)
    headers.pop("host", None)
    headers["referer"] = app.state.ACTIVEMQ_URL

    async with httpx.AsyncClient() as client:
        if request.method == "GET":
            resp = await client.get(target_url, headers=headers, params=request.query_params)
        else:
            body = await request.body()
            resp = await client.request(request.method, target_url, headers=headers, content=body)

    return Response(content=resp.content, status_code=resp.status_code, headers=resp.headers)
