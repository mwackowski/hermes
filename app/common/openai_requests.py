import requests
import json

from common._secrets import OPENAI_API_KEY  # pylint: disable=import-error


BASE_URL = "https://api.openai.com/v1/{endpoint}"

HEADER = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


def make_request(
    endpoint: str, data: dict = None, files: dict = None, header: dict = HEADER
):
    if not files:
        header["Content-Type"] = "application/json"
        resp = requests.post(
            BASE_URL.format(endpoint=endpoint), headers=header, data=json.dumps(data)
        )
    else:
        resp = requests.post(
            BASE_URL.format(endpoint=endpoint), headers=header, data=data, files=files
        )
    return json.loads(resp.text)


def send_moderations(input_msg: str):
    return make_request(endpoint="moderations", data={"input": input_msg})


def send_embeddings(input_msg: str, model_version: str):
    return make_request(
        endpoint="embeddings", data={"input": input_msg, "model": model_version}
    )


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
):
    return make_request(
        endpoint="chat/completions",
        data={
            "model": model_version,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        },
    )


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
