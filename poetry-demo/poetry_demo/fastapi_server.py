import asyncio
import json
from nats.aio.client import Client as NATS
from typing import Annotated, Dict

from fastapi import FastAPI, Header, HTTPException
from fastapi.openapi.utils import get_openapi

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

@app.patch("/coonect-nats")
async def connect_nats(nats_port,num, user_id: Annotated[str | None, Header()] = None,operator):
    await nc.connect(nats_port)
    subject = "calc"
    request_data = {
        "num": num,
        "user_id": user_id,
        "operator" :  operator
    }

    try:
        response = await nc.request(subject, json.dumps(request_data).encode(),timeout=30)
        response_data = json.loads(response.data.decode())
        result = response_data.get("result")
        return {"result": result}
    except Exception as e:
        print("An error occurred while communicating with the calculator service:", str(e))

if __name__ == "__main__":
    import uvicorn
    nc = NATS()
    uvicorn.run(app, host="0.0.0.0", port=8000)
