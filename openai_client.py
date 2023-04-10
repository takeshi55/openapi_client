import openai
import json
import os
import argparse
from datetime import datetime

def generate_text(prompt, model, history):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    with open('config/params.json', 'r', encoding='utf-8') as f:
        params = json.load(f)

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        **params
    )

    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default="gpt-3.5-turbo", help='The OpenAI model to use')
    parser.add_argument('--prompt', required=True, help='The text prompt for the model')
    parser.add_argument('--history_file', default=None, help='The file to store conversation history')
    args = parser.parse_args()

    history = []

    if args.history_file:
        history_file_path = os.path.join('history', args.history_file)
        if os.path.exists(history_file_path):
            with open(history_file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            with open(history_file_path, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)

    generated_text = generate_text(args.prompt, args.model, history)

    print(generated_text)

    history.append({"role": "user", "content": args.prompt})
    history.append({"role": "assistant", "content": generated_text})

    if args.history_file:
        with open(history_file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
