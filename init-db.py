import sqlite3, os

# データベースファイルのパス（環境変数で変更可能）
DB_PATH = os.environ.get('DB_PATH', '/data/markov.db')

# データディレクトリが存在しない場合は作成
db_dir = os.path.dirname(DB_PATH)
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

try:
    os.remove(DB_PATH)
except FileNotFoundError:
    print(f'{DB_PATH} not found, creating new database.')
except PermissionError:
    print(f'Cannot remove {DB_PATH} because file is in use or no permission.')
except Exception as e:
    print(f'Cannot remove {DB_PATH}: {e!r}')
    pass

db = sqlite3.connect(DB_PATH)

print('Initalizing database...', end='')

cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS model_data (acct TEXT NOT NULL PRIMARY KEY UNIQUE, data TEXT NOT NULL, allow_generate_by_other INTEGER NOT NULL)')
cur.close()

db.commit()
db.close()

print('OK')