# マルコフ連鎖ジェネレーター for Fediverse

MisskeyやMastodonの投稿を学習して、マルコフ連鎖による文章生成を行うWebアプリケーションです。

## バージョン

このプロジェクトには2つのバージョンがあります：

### 1. **Webアプリ版（Python）** - このREADME

サーバーで動作する本格的なWebアプリケーション。MeCabによる形態素解析を使用し、高品質な文章生成が可能です。

### 2. **[AiScript版](AISCRIPT_README.md)** - NEW! 🎉

Misskey内で直接動作するスクリプト版。**サーバー不要**で、Misskey Playですぐに実行できます！

👉 **[AiScript版の使い方はこちら](AISCRIPT_README.md)**

初めての方や、手軽に試したい方はAiScript版がおすすめです！

---

## 機能（Webアプリ版）

- **Fediverse対応**: MisskeyとMastodonの両方に対応
- **プライバシー設定**: 公開投稿のみ、フォロワー限定、ダイレクトまで対応
- **文章生成**: 学習した投稿から自然な文章を生成
- **権限管理**: 他のユーザーによる文章生成の許可/禁止設定

## セットアップ

### 1. 環境の準備

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
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

`config.py`は既に開発環境用の設定が含まれています。本番環境では以下の設定を変更してください：

```python
# 本番環境での推奨設定
PORT = 8888
DEBUG = False  # 本番環境ではFalseに設定
SECRET_KEY = 'your-production-secret-key-here'  # 本番環境では固定の秘密鍵を設定
MECAB_DICDIR = '/usr/lib/mecab/dic/unidic'  # 必要に応じて
MECAB_RC = '/etc/mecabrc'  # 必要に応じて
SENTRY_DSN = 'https://your-sentry-dsn@sentry.io/project-id'  # オプション
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