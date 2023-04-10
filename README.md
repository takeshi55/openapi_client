# OpenAI API Client for GPT-3.5-turbo

このレポジトリでは、OpenAI APIを使用してGPT-3.5-turboモデルと対話するためのPythonコマンドラインクライアントを提供しています。

## セットアップ

必要なパッケージをインストールします。

```
pip install openai
```

以下の環境変数を設定します。

```
export OPENAI_API_KEY=your_openai_api_key
```

## 使い方

コマンドライン引数を使用して、対話モデルに質問を投げることができます。

```
python3 openai_client.py --model "gpt-3.5-turbo" --prompt "What is the capital of France?"
```

```
--model: 使用するモデル名。デフォルトは "gpt-3.5-turbo" です。
--prompt: モデルに投げるプロンプト（質問）。
--history_file: 履歴ファイルへのパス。ファイルが存在しない場合は新規作成されます。
```

## パラメータの設定

config/params.json ファイルを編集して、APIリクエストのパラメータをカスタマイズできます。たとえば、temperature や max_tokens を変更できます。

