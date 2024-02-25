import json
from typing import ClassVar, Dict
import uvicorn
from fastapi import FastAPI, Query, Request

from config.logger_config import set_logger
from common.openai_requests import send_chat_completion
from common.utils import get_message
from common.databases import insert_into_knowledge_simple
from common.knowledge_manager import get_knowledge_data

logger = set_logger()


import os
import sys

from fastapi import FastAPI
from fastapi.logger import logger
from pydantic_settings import BaseSettings


def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass


app = FastAPI()


@app.get("/")
async def root():
    msg = "Welcome to Hermes App!"
    logger.info(msg)
    return msg


@app.post("/ownapi_task")
async def ownapi_task(input: Dict[str, str]):
    question, max_tokens = input.get("question"), input.get("max_tokens")
    if not question:
        return {"message": "Question field not found."}

    max_tokens = min(int(max_tokens), 100)

    ai_resp = send_chat_completion(
        "gpt-3.5-turbo", user_content=question, max_tokens=max_tokens
    )

    return {"reply": get_message(ai_resp)}


@app.post("/ownapipro_task")
async def ownapipro_task(input: Dict[str, str]):
    question, max_tokens = input.get("question"), input.get("max_tokens")

    if max_tokens:
        max_tokens = min(int(max_tokens), 100)

    if "?" in question:
        knowledge_data = get_knowledge_data()
        ai_resp = send_chat_completion(
            "gpt-3.5-turbo",
            system_content=f"Provide information using following context in the first place:\n###Context: {knowledge_data}\nBe concise.",
            user_content=question,
            max_tokens=max_tokens,
        )
        msg = f"U: {question}\A-: {get_message(ai_resp)}"
        insert_into_knowledge_simple(msg)
        logger.info(ai_resp)
        return {"reply": get_message(ai_resp)}
    else:
        insert_into_knowledge_simple(question, source="USER")
        return {"reply": "Saved into knowledge db."}


if __name__ == "__main__":
    settings = BaseSettings()
    if os.environ.get("USE_NGROK") and os.environ.get("NGROK_AUTHTOKEN"):
        # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
        from pyngrok import ngrok

        # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
        # when starting the server
        port = (
            sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else "8080"
        )
        # Open a ngrok tunnel to the dev server
        print(f"port: {port}")
        public_url = ngrok.connect(port).public_url
        print(f'ngrok tunnel "{public_url}" -> "http://127.0.0.1:{port}')

        # init_webhooks(public_url)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        workers=1,
        proxy_headers=True,
    )
