# 本番環境用設定ファイル
# 環境変数から設定を読み込みます

import os

# Webサーバーの待ち受けポート
PORT = int(os.environ.get('PORT', 8888))

# デバッグモードで起動するか (本番環境ではFalse)
DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']

# MeCabで使用する辞書があるディレクトリの絶対パス
MECAB_DICDIR = os.environ.get('MECAB_DICDIR', None)

# mecabrcの絶対パス
MECAB_RC = os.environ.get('MECAB_RC', None)

# Sentry DSN (エラー監視用、オプション)
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

# セッションキー (本番環境では環境変数から読み取る)
# fly secrets set SECRET_KEY=your-secret-key-here で設定してください
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')
