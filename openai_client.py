import openai
import argparse
import json
import os
import uuid

# openai.api_key を環境変数から読み込む
openai.api_key = os.environ["OPENAI_API_KEY"]

def create_history_file(file_path):
    initial_history = {"messages": [{"role": "system", "content": "You are a helpful assistant."}]}
    with open(file_path, "w") as f:
        json.dump(initial_history, f, ensure_ascii=False, indent=2)
    print(f"Created a new history file: {file_path}")

def load_history(file_path):
    if not os.path.exists(file_path):
        create_history_file(file_path)
        
    with open(file_path, "r") as f:
        history = json.load(f)
    return history["messages"]

def save_history(file_path, history):
    with open(file_path, "w") as f:
        json.dump({"messages": history}, f, ensure_ascii=False, indent=2)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate text using OpenAI API.")
    parser.add_argument("--model", default="gpt-3.5-turbo", type=str, help="Name of the model to use.")
    parser.add_argument("--prompt", default="What is the capital of France?", type=str, help="The text prompt to generate text from.")
    args = parser.parse_args()

    unique_id = str(uuid.uuid4())
    history_file = f"history_{unique_id}.json"
    history = load_history(history_file)
    generated_text = generate_text(args.prompt, args.model, history)
    
    # Update the conversation history with the user's input and model's response
    history.append({"role": "user", "content": args.prompt})
    history.append({"role": "assistant", "content": generated_text})
    
    # Save the updated history to the file
    save_history(history_file, history)

    print(generated_text)
