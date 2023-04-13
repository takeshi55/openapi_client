 # OpenAIチャットクライアント

このコードは、OpenAI APIを使用してチャットボットを作成するためのものです。ユーザーが入力したテキストに対して、OpenAIのモデルを使用して応答を生成します。また、会話の履歴を保存することもできます。

## 使い方

1. `config/params.json`ファイルを編集して、使用するOpenAIモデルとその他のパラメータを設定します。
2. `OPENAI_API_KEY`環境変数に、OpenAI APIのAPIキーを設定します。
3. `python openai_client.py`を実行して、チャットボットを起動します。
4. ユーザーが入力したテキストに対して、チャットボットが応答を生成します。
5. `Ctrl+X`を押すとチャットボットにテキストを送信できます。
6. `Ctrl+C`を押して、会話を終了します。

## コマンドライン引数

- `--model`: 使用するOpenAIモデルを指定します。デフォルトは`gpt-3.5-turbo`です。
- `--history_file`: 会話の履歴を保存するファイルのパスを指定します。ファイルを読み込ませることでスレッドとして使用できます。
- `--config_file`: パラメータを含むJSONファイルのパスを指定します。デフォルトは`params.json`です。

## 依存関係

- OpenAI API
- tiktoken
- argparse
- datetime
- json
- os
- sys
- termios
- tty

 ## 関数

### `wait_input()`

ユーザーからの入力を待ち、入力されたテキストを返します。`Ctrl+X`を押すと、入力されたテキストが返されます。

### `num_tokens_from_messages(messages, model)`

与えられたメッセージのリストから、使用されるトークンの数を計算して返します。使用するOpenAIモデルに応じて、トークン数の計算方法が異なります。

### `generate_text(prompt, model, history, params, history_file_path)`

与えられたプロンプトに対して、OpenAIモデルを使用して応答を生成します。また、会話の履歴を更新します。

### `main()`

コマンドライン引数を解析し、チャットボットを起動します。ユーザーからの入力を待ち、応答を生成します。また、会話の履歴を保存します。

## 注意事項

- このコードを実行するには、OpenAI APIのAPIキーが必要です。
- このコードは、Python 3で動作します。
