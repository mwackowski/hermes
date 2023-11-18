import textwrap


def get_message(ai_response):
    """Return a message from ai response.

    Exemplary response to retrieve message from:
    {'id': 'chatcmpl-8GDWNsy3CKLCdKBYpt9P8dEizzU0x',
    'object': 'chat.completion',
    'created': 1698875915,
    'model': 'gpt-4-0613',
    'choices': [{'index': 0,
    'message': {'role': 'assistant', 'content': 'Alojzy'},
    'finish_reason': 'stop'}],
    'usage': {'prompt_tokens': 75, 'completion_tokens': 4, 'total_tokens': 79}}
    """
    return ai_response["choices"][0]["message"]["content"]


def print_task(task, print_len=150):
    for k, v in task.items():
        print(k)
        wrapped = textwrap.wrap(str(v), print_len)
        print("\n".join(wrapped))
        print("*" * print_len)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]
