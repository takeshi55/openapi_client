import openai
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

def generate_text(prompt, model, history):
    response = openai.ChatCompletion.create(
        model=model,
        messages=history + [{"role": "user", "content": prompt}],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.1,
    )
    return response.choices[0].message['content'].strip()

def load_history(history_path):
    if history_path.exists():
        with open(history_path, "r") as f:
            history = json.load(f)
    else:
        history = [{"role": "system", "content": "You are a helpful assistant."}]
        with open(history_path, "w") as f:
            json.dump(history, f)
        print(f"Created a new history file: {history_path.name}")
    return history

def save_history(history_path, history):
    with open(history_path, "w") as f:
        json.dump(history, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OpenAI API Client for GPT-3.5-turbo")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model name")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt text")
    parser.add_argument("--history_file", type=str, help="Path to the history file")

    args = parser.parse_args()

    openai.api_key = os.getenv("OPENAI_API_KEY")

    if args.history_file:
        history_path = Path("history") / args.history_file
    else:
        history_path = Path("history") / f"history_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    history = load_history(history_path)
    generated_text = generate_text(args.prompt, args.model, history)
    history.append({"role": "assistant", "content": generated_text})
    save_history(history_path, history)

    print("Generated text:")
    print(generated_text)
