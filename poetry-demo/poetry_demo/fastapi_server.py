import asyncio
import json
import os
import nats
import argparse  # Import argparse for command-line argument parsing
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
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

# Default NATS port value
DEFAULT_NATS_PORT = 4222

# Add a command-line argument for NATS port
parser = argparse.ArgumentParser(description="FastAPI app with NATS integration")
parser.add_argument("--nats-port", type=int, default=DEFAULT_NATS_PORT, help="NATS server port")

@app.get("/connect-nats")
async def connect_nats(num: str = Header(None),operator: str = Header(None),
    user_id: str = Header(None),port: str = Header("4222")
):
    global nats_port  # Access the global variable
    subject = "calc"
    request_data = {
        "num": num,
        "user_id": user_id,
        "operator": operator,
        "port" : port
        
    }
    await nc.connect(f"nats://{nats_server_address}:{port}")  # Updated connection to use environment variable


    try:
        response = await nc.request(subject, json.dumps(request_data).encode(), timeout=30)
        response_data = json.loads(response.data.decode())
        result = response_data.get("result")
        await nc.close()
        return {"result": result}
    except Exception as e:
        print("An error occurred while communicating with the calculator service:", str(e))

if __name__ == "__main__":
    import uvicorn
    nc = NATS()

    # Read the NATS server address from the environment variable
    nats_server_address = os.environ.get("NATS_SERVER_ADDRESS", "localhost")

    

    uvicorn.run(app, host="0.0.0.0", port=8000)
