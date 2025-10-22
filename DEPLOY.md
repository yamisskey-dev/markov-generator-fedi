# Fly.ioへのデプロイ手順

このドキュメントでは、マルコフ連鎖ジェネレーター for Fediverseを**Fly.io**にデプロイする手順を説明します。

## 前提条件

- Fly.ioアカウント（無料で作成可能）
- `flyctl` CLIツールのインストール

## 1. Fly.io CLIのインストール

### macOS / Linux
```bash
curl -L https://fly.io/install.sh | sh
```

### Windows (PowerShell)
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

インストール後、パスを通してください。

## 2. Fly.ioにログイン

```bash
flyctl auth login
```

ブラウザが開き、認証画面が表示されます。

## 3. アプリケーションの作成

プロジェクトディレクトリで以下を実行：

```bash
flyctl launch
```

以下のように回答してください：

- **App name**: `markov-generator-fedi` （または任意の名前）
- **Organization**: Personal（または任意の組織）
- **Region**: `nrt` (Tokyo, Japan) を選択
- **Would you like to set up a PostgreSQL database?**: **No**
- **Would you like to set up an Upstash Redis database?**: **No**
- **Would you like to deploy now?**: **No** (設定を確認してから)

## 4. 永続ボリュームの作成

SQLiteデータベース用の永続ボリュームを作成します：

```bash
flyctl volumes create markov_data --region nrt --size 1
```

- `markov_data`: ボリューム名（fly.tomlと一致させる）
- `--region nrt`: 東京リージョン
- `--size 1`: 1GB（無料枠内）

## 5. シークレットの設定

セッション用のシークレットキーを設定します：

```bash
# ランダムなシークレットキーを生成
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

出力されたキーをコピーして、以下を実行：

```bash
flyctl secrets set SECRET_KEY="生成されたキーをここに貼り付け"
```

### オプション: Sentryの設定

エラー監視にSentryを使う場合：

```bash
flyctl secrets set SENTRY_DSN="your-sentry-dsn-here"
```

## 6. fly.tomlの確認

`fly.toml`ファイルが正しく設定されているか確認してください：

```toml
app = "markov-generator-fedi"  # 実際のアプリ名に合わせる
primary_region = "nrt"

[mounts]
  source = "markov_data"
  destination = "/data"
  initial_size = "1gb"
```

## 7. デプロイ

```bash
flyctl deploy
```

初回デプロイには5〜10分かかります（Dockerイメージのビルドとプッシュ）。

## 8. アプリケーションの確認

デプロイが完了したら、以下で確認できます：

```bash
# アプリのURLを開く
flyctl open

# ログを確認
flyctl logs

# ステータス確認
flyctl status

# SSHでコンテナに接続
flyctl ssh console
```

## 9. カスタムドメインの設定（オプション）

独自ドメインを使う場合：

```bash
# 証明書の作成
flyctl certs create example.com

# DNSレコードを設定（表示される指示に従う）
flyctl certs show example.com
```

## トラブルシューティング

### データベースが初期化されない

```bash
# SSHでコンテナに接続
flyctl ssh console

# 手動で初期化
cd /app
python3 init-db.py
```

### アプリが起動しない

```bash
# ログを確認
flyctl logs

# リージョンとボリュームが一致しているか確認
flyctl volumes list
flyctl status
```

### ボリュームが接続されない

```bash
# ボリュームを削除して再作成
flyctl volumes list
flyctl volumes delete vol_xxxxx
flyctl volumes create markov_data --region nrt --size 1

# 再デプロイ
flyctl deploy
```

## スケーリング

### メモリを増やす

```bash
flyctl scale memory 1024  # 1GBに増やす
```

### CPUを増やす

```bash
flyctl scale vm shared-cpu-2x  # 2xに増やす
```

## コスト管理

無料枠を維持するには：

- VM: shared-cpu-1x, 256MB RAM（無料）
- ボリューム: 3GB以下（無料）
- 自動停止を有効化（fly.tomlで設定済み）

## 更新

コードを更新した場合：

```bash
git add .
git commit -m "Update"
flyctl deploy
```

## アプリの削除

不要になった場合：

```bash
# ボリュームを削除
flyctl volumes list
flyctl volumes delete vol_xxxxx

# アプリを削除
flyctl apps destroy markov-generator-fedi
```

## サポート

- [Fly.io公式ドキュメント](https://fly.io/docs/)
- [Fly.io Communityフォーラム](https://community.fly.io/)
