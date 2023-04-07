import openai
import argparse
import os

def generate_text(prompt, model):
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "あなたはねこ娘です。語尾にニャンをつけて話します。仕事に関してはとても厳しく真面目です"}, {"role": "user", "content": prompt}],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.9,
    )

    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GPT-3 based client for text generation.")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="Model to use for text generation")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to send to the model")
    args = parser.parse_args()

    generated_text = generate_text(args.prompt, args.model)
    print(generated_text)
