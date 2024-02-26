import os
import sys
from typing import Dict
from threading import Thread

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from common.openai_requests import send_chat_completion
from common.utils import get_message
from common.message_parser import handle_message, verify_user_id
from config.logger_config import set_logger
from config.const import GPT_4, GPT_3_5, GPT_4_TURBO

load_dotenv()


logger = set_logger()





def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


def engrok_setup():
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8080"
    public_url = ngrok.connect(port).public_url
    msg_info = f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:{port}"'
    logger.info(msg_info)

    settings.BASE_URL = public_url
    with open("config/engrok_url", "w") as f:
        f.write(public_url)
    init_webhooks(public_url)


app = FastAPI()

if os.environ.get("NGROK_AUTHTOKEN"):
    class Settings(BaseSettings):
        USE_NGROK: bool = os.environ.get("USE_NGROK", "False") == "True"
        BASE_URL: str = "http://localhost:8080"
        
    settings = Settings()
    engrok_setup()


@app.get("/")
async def root():
    msg = "Welcome to Hermes App!"
    logger.info(msg)
    return msg


@app.get("/healthcheck")
def get_healthcheck():
    return {"server": "up"}


def handle_response(data: Dict, resp: Response):  
    user = data["event"]["user"]
    if not verify_user_id(user):
        return f"User: {user} not identified"
    
    resp.status_code = status.HTTP_202_ACCEPTED
    return resp


@app.router.post("/api/slack-webhook")
async def slack_webhook(resp: Response, data: Dict):
  
    logger.info(data)
    if data['type'] == "url_verification":
        return data["challenge"]
    
    if data['type'] == 'event_callback' and not data['event'].get('bot_id'):
        t = Thread(target=handle_message, args=(data,))
        t.start()
        
    handle_response(data, resp)

    



# uvicorn main:app --host 0.0.0.0 --port 8080
