from logging import Logger
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


BASE_URL = "https://api.openai.com/v1/{endpoint}"

HEADER = {
    "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
}


def make_request(
    endpoint: str,
    data: dict = None,
    files: dict = None,
    header: dict = HEADER,
    method: str = "POST",
):
    req = {
        "POST": {"fn": requests.post, "data": json.dumps(data)},
        "GET": {"fn": requests.get, "data": data},
    }[method]
    fn, data = req["fn"], req["data"]

    if not files:
        header["Content-Type"] = "application/json"
        resp = fn(BASE_URL.format(endpoint=endpoint), headers=header, data=data)
    else:
        resp = fn(
            BASE_URL.format(endpoint=endpoint), headers=header, data=data, files=files
        )
    return json.loads(resp.text)


def send_moderations(input_msg: str):
    return make_request(endpoint="moderations", data={"input": input_msg})


def send_embeddings(input_msg: str, model_version: str):
    return make_request(
        endpoint="embeddings", data={"input": input_msg, "model": model_version}
    )


def get_models():
    return make_request(endpoint="models", method="GET")


def send_transcription(
    audo_file_name: str,
    audio_file: bytes,
    language: str,
    response_format: str = "json",
    model: str = "whisper-1",
    temperature: float = 0,
):
    return make_request(
        endpoint="audio/transcriptions",
        files={
            "file": (audo_file_name, audio_file),
        },
        data={
            "model": model,
            "language": language,
            "temperature": temperature,
            "response_format": response_format,
        },
    )


def send_chat_completion(
    model_version: str = "",
    system_content: str = "",
    user_content: str = "",
    temperature: float = 0,
    max_tokens: int = 0,
    logger: Logger = None
):
    data = {
        "model": model_version,
        "messages": [
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
    }
    if system_content:
        data['messages'].insert(0, {"role": "system", "content": system_content})
    if max_tokens:
        data["max_tokens"] = max_tokens
    if logger:
        logger.info(f'Request for openai:\n{data}')
    return make_request(endpoint="chat/completions", data=data)


def send_vision_request(
    user_input, image_url, max_tokens=300, model="gpt-4-vision-preview"
):
    return make_request(
        endpoint="chat/completions",
        data={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_input},
                        {"type": "image_url", "image_url": {"url": image_url}},
                    ],
                }
            ],
            "max_tokens": max_tokens,
        },
    )
