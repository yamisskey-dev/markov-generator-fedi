# マルコフ連鎖ジェネレーター for Fediverse

MisskeyやMastodonの投稿を学習して、マルコフ連鎖による文章生成を行うWebアプリケーションです。

## 機能

- **Fediverse対応**: MisskeyとMastodonの両方に対応
- **プライバシー設定**: 公開投稿のみ、フォロワー限定、ダイレクトまで対応
- **文章生成**: 学習した投稿から自然な文章を生成
- **権限管理**: 他のユーザーによる文章生成の許可/禁止設定

## セットアップ

### 1. 環境の準備

```bash
# 仮想環境の作成
python3 -m venv env
source env/bin/activate  # Linux/Mac
# または
env\Scripts\activate  # Windows

# 依存関係のインストール
pip install -r requirements.txt

# MeCab辞書のダウンロード
python3 -m unidic download
```

### 2. 設定ファイルの作成

```bash
# 設定ファイルテンプレートをコピー
cp config.py.example config.py
```

`config.py`を編集して、以下の設定を行ってください：

```python
# Webサーバーの待ち受けポート
PORT = 8888

# デバッグモード（本番環境ではFalse推奨）
DEBUG = True

# MeCab辞書のパス（必要に応じて）
MECAB_DICDIR = '/usr/lib/mecab/dic/unidic'
MECAB_RC = '/etc/mecabrc'

# Sentry DSN（エラー監視用、オプション）
SENTRY_DSN = 'https://your-sentry-dsn@sentry.io/project-id'

# セッションキー（本番環境では固定の秘密鍵を設定）
SECRET_KEY = 'your-secret-key-here'
```

### 3. データベースの初期化

```bash
python3 init-db.py
```

### 4. アプリケーションの起動

```bash
python3 web.py
```

ブラウザで `http://localhost:8888` にアクセスしてください。

## 使用方法

1. **ログイン**: MisskeyまたはMastodonのアカウントでログイン
2. **学習**: 投稿データを取得してマルコフモデルを作成
3. **生成**: 学習したデータから文章を生成

## API エンドポイント

- `GET /` - メインページ
- `POST /login` - ログイン処理
- `GET /login/callback` - OAuth認証コールバック
- `GET /generate` - 文章生成ページ
- `GET /generate/do` - 文章生成実行
- `POST /my/delete-model-data` - 学習データ削除
- `GET /privacy` - プライバシーポリシー
- `GET /logout` - ログアウト

## テスト

```bash
# 単体テストの実行
python3 -m unittest test_markov_model.py
python3 -m unittest test_database.py

# 全テストの実行
python3 -m unittest discover
```

## セキュリティ

- セッションキーは本番環境では固定の秘密鍵を設定してください
- SQLインジェクション対策としてパラメータ化クエリを使用
- 入力値の検証とサニタイゼーションを実装

## ライセンス

Copyright 2022 CyberRex

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 作者

Created by CyberRex (@cyberrex_v2@misskey.io)