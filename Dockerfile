# Python 3.11ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリ設定
WORKDIR /app

# システムパッケージのインストール
RUN apt-get update && apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    git \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピー
COPY requirements.txt .

# Pythonパッケージのインストール
RUN pip install --no-cache-dir -r requirements.txt

# UniDic辞書のダウンロード
RUN python3 -m unidic download

# アプリケーションファイルをコピー
COPY . .

# データベース用ディレクトリ作成（初期化用、実際はボリュームマウント）
RUN mkdir -p /data

# エントリーポイントスクリプトを作成
RUN echo '#!/bin/bash\n\
# データベースが存在しない場合のみ初期化\n\
if [ ! -f /data/markov.db ]; then\n\
  echo "Initializing database..."\n\
  python3 init-db.py\n\
fi\n\
# Gunicornでアプリケーションを起動\n\
exec gunicorn --bind 0.0.0.0:8888 --workers 2 --threads 4 --timeout 120 web:app\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# ポート8888を公開
EXPOSE 8888

# エントリーポイントを設定
ENTRYPOINT ["/entrypoint.sh"]
