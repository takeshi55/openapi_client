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
    parser.add_argument('--history_file', default="my_history.json", help='The file to store conversation history')
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
    else:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        args.history_file = f"history_{timestamp}.json"
        history_file_path = os.path.join('history', args.history_file)
        with open(history_file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    print("To end the conversation, press Ctrl+C.")

    try:
        while True:
            prompt = input("You: ")
            generated_text = generate_text(prompt, args.model, history)

            print(f"Assistant: {generated_text}")

            history.append({"role": "user", "content": prompt})
            history.append({"role": "assistant", "content": generated_text})

            if args.history_file:
                with open(history_file_path, 'w', encoding='utf-8') as f:
                    json.dump(history, f, ensure_ascii=False, indent=2)
    except KeyboardInterrupt:
        print("\nConversation ended by user.")
