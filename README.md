# 概要

このスクリプトは、OpenAI APIを利用してGPT-3.5-turboモデルと対話するためのPythonプログラムです。

## 必要なパッケージ

```
openai
json
os
argparse
datetime
```

## インストール方法
Python 3.x がインストールされていることを確認してください。
pip install openai で openai パッケージをインストールします。

## 使い方
OpenAI APIキーを環境変数に設定してください。例: export OPENAI_API_KEY=your_api_key
python3 openai_client.py を実行してください。会話を終了する場合は、Ctrl + Cを押して強制終了します。

### オプション
--model: 使用するOpenAIモデルを指定します。デフォルトは "gpt-3.5-turbo" です。
--history_file: 会話履歴を保存するファイル名を指定します。存在しない場合は新しく作成されます。指定しない場合は、自動的に一意のファイル名が生成されます。

### 注意
このスクリプトは、OpenAI APIの利用に関連する費用が発生する場合があります。詳細については、OpenAIの料金表をご確認ください。
会話中に生成されるテキストは、GPT-3.5-turboモデルが生成したものであり、必ずしも正確ではないことに注意してください。