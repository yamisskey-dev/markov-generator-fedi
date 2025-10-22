# Fly.ioへのデプロイ手順

このドキュメントでは、マルコフ連鎖ジェネレーター for Fediverseを**Fly.io**にデプロイする手順を説明します。

## 前提条件

- Fly.ioアカウント（無料で作成可能）
- `flyctl` CLIツールのインストール（または、Fly.io Web UIを使用）

## デプロイ方法

### 方法1: Fly.io Web UI（推奨）

#### 1. Fly.ioにサインアップ

https://fly.io にアクセスしてGitHubアカウントでサインアップ

#### 2. GitHub連携でデプロイ

1. Fly.ioダッシュボードで「**Deploy**」をクリック
2. 「**Choose a repository**」からこのリポジトリを選択
3. App name: `markov-generator-fedi` （または任意の名前）
4. Organization: Personal
5. **「Deploy」をクリック**

#### 3. デプロイ完了後の設定

##### ボリュームの作成（必須）

**方法A: ブラウザから作成**

1. `https://fly.io/dashboard/[your-app-name]/volumes` にアクセス
2. 「**Create Volume**」をクリック
3. 以下を入力：
   - Name: `markov_data`
   - Region: `Tokyo, Japan (nrt)`
   - Size: `1 GB`
4. 保存

**方法B: Windows PowerShellから作成**

```powershell
# PowerShellで実行
flyctl volumes create markov_data --app markov-generator-fedi --region nrt --size 1
```

##### SECRET_KEYの設定（必須）

1. `https://fly.io/dashboard/[your-app-name]/secrets` にアクセス
2. 「**New secret**」をクリック
3. 以下を入力：
   ```
   Name: SECRET_KEY
   Value: （ランダムな文字列）
   ```

**シークレットキーの生成方法：**

```bash
# Linux/Mac/WSL
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# または
openssl rand -base64 32
```

Windows PowerShellの場合：
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

出力された文字列をコピーして、Secretsに貼り付けてください。

##### アプリの再起動

1. ダッシュボードの「**Overview**」に戻る
2. 右上の「**Restart**」ボタンをクリック

---

### 方法2: Fly.io CLI（Windows PowerShell推奨）

#### 1. flyctl CLIのインストール

**Windows PowerShell:**
```powershell
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

**macOS/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

#### 2. ログイン

```bash
flyctl auth login
```

ブラウザが開いて認証されます。

#### 3. アプリの作成とデプロイ

```bash
# プロジェクトディレクトリに移動
cd /path/to/markov-generator-fedi

# アプリを作成（初回のみ）
flyctl launch

# デプロイ
flyctl deploy
```

#### 4. ボリュームの作成

```bash
flyctl volumes create markov_data --app markov-generator-fedi --region nrt --size 1
```

#### 5. SECRET_KEYの設定

```bash
# シークレットキーを生成
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 出力されたキーを設定
flyctl secrets set SECRET_KEY="生成されたキーをここに貼り付け" --app markov-generator-fedi
```

#### 6. 再デプロイ

```bash
flyctl deploy --app markov-generator-fedi
```

---

## デプロイ後の確認

### アプリへのアクセス

```bash
flyctl open --app markov-generator-fedi
```

または、ブラウザで以下にアクセス：
```
https://markov-generator-fedi.fly.dev
```

### ログの確認

```bash
flyctl logs --app markov-generator-fedi
```

### ステータス確認

```bash
flyctl status --app markov-generator-fedi
```

### SSHでコンテナに接続

```bash
flyctl ssh console --app markov-generator-fedi
```

---

## トラブルシューティング

### ボリュームが接続されない

```bash
# ボリュームのリスト確認
flyctl volumes list --app markov-generator-fedi

# ボリュームとアプリのリージョンが一致しているか確認
flyctl status --app markov-generator-fedi

# 再デプロイ
flyctl deploy --app markov-generator-fedi
```

### データベースエラーが出る

```bash
# SSHで接続
flyctl ssh console --app markov-generator-fedi

# データベースを手動で初期化
cd /app
python3 init-db.py
```

### WSLでflyctl認証エラー

**方法A: Web UIからトークンを取得**

1. https://fly.io/user/personal_access_tokens にアクセス
2. 「Create Token」をクリック
3. トークンをコピー
4. WSLで設定：
   ```bash
   export FLY_API_TOKEN="コピーしたトークン"
   ```

**方法B: Windows PowerShellを使う**

WSLではなく、Windows PowerShellでflyctlコマンドを実行してください。

---

## カスタムドメインの設定（オプション）

```bash
# 証明書の作成
flyctl certs create example.com --app markov-generator-fedi

# DNSレコードの確認
flyctl certs show example.com --app markov-generator-fedi
```

表示されたDNSレコードをドメインのDNS設定に追加してください。

---

## スケーリング

### メモリを増やす

```bash
flyctl scale memory 1024 --app markov-generator-fedi
```

### CPUを増やす

```bash
flyctl scale vm shared-cpu-2x --app markov-generator-fedi
```

---

## コスト管理

### 無料枠を維持するには：

- VM: shared-cpu-1x（無料）
- ボリューム: 3GB以下（無料）
- 自動停止を有効化（fly.tomlで設定済み）

---

## アプリの削除

```bash
# ボリュームを削除
flyctl volumes list --app markov-generator-fedi
flyctl volumes delete vol_xxxxx

# アプリを削除
flyctl apps destroy markov-generator-fedi
```

---

## サポート

- [Fly.io公式ドキュメント](https://fly.io/docs/)
- [Fly.io Communityフォーラム](https://community.fly.io/)
