from typing import Dict
import uvicorn
from fastapi import FastAPI, Query, Request

from config.logger_config import set_logger
from common.openai_requests import send_chat_completion
from common.utils import get_message
from common.databases import insert_into_knowledge_simple

logger = set_logger()


app = FastAPI()


@app.get("/")
async def root():
    msg = "Welcome to Hermes App!"
    logger.info(msg)
    return msg


@app.post("/ownapi_task")
async def ownapi_task(input: Dict[str, str]):
    logger.info(input)
    question, max_tokens = input.get("question"), input.get("max_tokens")
    if not question:
        return {"message": "Question field not found."}
    if max_tokens:
        max_tokens = min(int(max_tokens), 100)

    ai_resp = send_chat_completion(
        "gpt-3.5-turbo", user_content=question, max_tokens=max_tokens
    )
    logger.info(ai_resp)
    return {"reply": get_message(ai_resp)}


@app.post("/ownapipro_task")
async def ownapipro_task(input: Dict[str, str]):
    logger.info(input)
    question, max_tokens = input.get("question"), input.get("max_tokens")
    if not question:
        return {"message": "Question field not found."}
    if max_tokens:
        max_tokens = min(int(max_tokens), 100)

    if question.endswith('?'):
        logger.info('processing in AI')
        # ai_resp = send_chat_completion(
        # "gpt-3.5-turbo", user_content=question, max_tokens=max_tokens
        # )
        # logger.info(ai_resp)
    else:
        insert_into_knowledge_simple()


    return {"reply": 'done'}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1,
        proxy_headers=True,
    )
