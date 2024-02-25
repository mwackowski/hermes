import json
from logging import Logger
from typing import Dict
from common.slack_handler import send_message
from common.prompts import INTENT_IDENTIFICATION, TEXT_VERIFICATION, TRANSLATION, CODE_ASSISTANT

from common.openai_requests import send_chat_completion
from common.utils import get_message
from config.const import GPT_4, GPT_3_5, GPT_4_TURBO
from config.logger_config import set_logger


logger = set_logger()
# store it elsewhere - either in config file or db
MY_USER_ID = "U06K2N0A4N4"


def verify_user_id(user: str):
    return user == MY_USER_ID


def get_text_from_slack_event(data: Dict):
    return data["event"]["text"]


def handle_intentions(actions_response, user_message):
    action = actions_response["action"]
    prompts = {
        'translate': TRANSLATION,
        'verify': TEXT_VERIFICATION,
        'code assist': CODE_ASSISTANT
    }

    ai_resp = send_chat_completion(
        model_version=GPT_4,
        user_content=user_message,
        system_content=prompts.get(action)
    )
    return get_message(ai_resp)


def identify_intent(message):
    ai_resp = send_chat_completion(
        model_version=GPT_4,
        user_content=' '.join(message.split()[:5]),
        system_content=INTENT_IDENTIFICATION,
        max_tokens=100,
        logger=logger
    )
    return get_message(ai_resp)


def handle_message(data: Dict):
    message = get_text_from_slack_event(data)
    if len(message) <= 3:
        send_message("The command is not clear")
        return

    # ai_resp = send_chat_completion(
    #     model_version=GPT_3_5,
    #     user_content=' '.join(message.split()[:5]),
    #     system_content=INTENT_IDENTIFICATION,
    #     max_tokens=100,
    #     logger=logger
    # )
    # logger.info(ai_resp)
    # ai_msg = get_message(ai_resp)
    ai_msg = identify_intent(message)

    try:
        actions = json.loads(ai_msg)
    except json.JSONDecodeError:
        send_message(ai_msg)
        return
    
    logger.info(f'Actions identified: {actions}')
    ai_resp2 = handle_intentions(actions, message)
    send_message(ai_resp2)

