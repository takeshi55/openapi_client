import os
import json
import argparse
from datetime import datetime
import openai
from openai import ChatCompletion
import tiktoken
from tiktoken.core import Encoding

def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows {role/name}\n{content}\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with assistant
    return num_tokens
    
def generate_text(prompt, model, history, params, history_file_path):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    total_tokens = num_tokens_from_messages(messages, model)
    while total_tokens > 3048:
        print("Token limit detected! Delete history..." + str(total_tokens))

        messages.pop(0)
        total_tokens = num_tokens_from_messages(messages, model)

    response = ChatCompletion.create(
        model=model,
        messages=messages,
        **params
    )

    generated_text = response.choices[0].message['content'].strip()

    if history_file_path:
        with open(history_file_path, 'w', encoding='utf-8') as f:
            while num_tokens_from_messages(history, model) > 3048:
                history.pop(0)
            json.dump(history, f, ensure_ascii=False, indent=2)

    return generated_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default="gpt-3.5-turbo", help='The OpenAI model to use')
    parser.add_argument('--history_file', default=None, help='The file to store conversation history')
    args = parser.parse_args()

    openai.api_key = os.environ["OPENAI_API_KEY"]

    with open('config/params.json', 'r', encoding='utf-8') as f:
        params = json.load(f)

    history_file_path = None

    if args.history_file:
        history_file_path = os.path.join('history', args.history_file)
        if not os.path.exists(history_file_path):
            with open(history_file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    else:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        args.history_file = f"history_{timestamp}.json"
        history_file_path = os.path.join('history', args.history_file)
        with open(history_file_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    if history_file_path:
        with open(history_file_path, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    print("To end the conversation, press Ctrl+C.")

    try:
        while True:
            prompt = input("You: ")
            generated_text = generate_text(prompt, args.model, history, params, history_file_path)

            print(f"Assistant: {generated_text}")

            history.append({"role": "user", "content": prompt})
            history.append({"role": "assistant", "content": generated_text})

            if history_file_path:
                with open(history_file_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
    except KeyboardInterrupt:
        print("\nConversation ended by user.")
    finally:
        if history_file_path:
            with open(history_file_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()