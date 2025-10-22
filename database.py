"""
データベース操作を管理するモジュール
"""
import sqlite3
import traceback
from typing import Optional, Dict, Any


def dict_factory(cursor, row):
    """SQLiteの結果を辞書形式で返すファクトリー関数"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DatabaseManager:
    """データベース操作を管理するクラス"""
    
    def __init__(self, db_path: str = '/data/markov.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = dict_factory
    
    def get_connection(self):
        """データベース接続を取得"""
        return self.connection
    
    def save_model_data(self, acct: str, model_data: str, allow_generate_by_other: bool) -> bool:
        """マルコフモデルデータを保存"""
        try:
            cur = self.connection.cursor()
            cur.execute('DELETE FROM model_data WHERE acct = ?', (acct,))
            cur.execute('INSERT INTO model_data(acct, data, allow_generate_by_other) VALUES (?, ?, ?)', 
                       (acct, model_data, int(allow_generate_by_other)))
            cur.close()
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Failed to save model data: {e}")
            print(traceback.format_exc())
            return False
    
    def get_model_data(self, acct: str) -> Optional[Dict[str, Any]]:
        """マルコフモデルデータを取得"""
        try:
            cur = self.connection.cursor()
            cur.execute('SELECT data FROM model_data WHERE acct = ?', (acct,))
            result = cur.fetchone()
            cur.close()
            return result
        except Exception as e:
            print(f"Failed to get model data: {e}")
            return None
    
    def get_model_permissions(self, acct: str) -> Optional[Dict[str, Any]]:
        """モデルの生成許可設定を取得"""
        try:
            cur = self.connection.cursor()
            cur.execute('SELECT allow_generate_by_other FROM model_data WHERE acct = ?', (acct,))
            result = cur.fetchone()
            cur.close()
            return result
        except Exception as e:
            print(f"Failed to get model permissions: {e}")
            return None
    
    def delete_model_data(self, acct: str) -> bool:
        """マルコフモデルデータを削除"""
        try:
            cur = self.connection.cursor()
            cur.execute('DELETE FROM model_data WHERE acct = ?', (acct,))
            cur.close()
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Failed to delete model data: {e}")
            return False
    
    def model_exists(self, acct: str) -> bool:
        """モデルデータが存在するかチェック"""
        try:
            cur = self.connection.cursor()
            cur.execute('SELECT COUNT(*) FROM model_data WHERE acct = ?', (acct,))
            result = cur.fetchone()
            cur.close()
            return result['COUNT(*)'] > 0
        except Exception as e:
            print(f"Failed to check model existence: {e}")
            return False
    
    def close(self):
        """データベース接続を閉じる"""
        if self.connection:
            self.connection.close()


# グローバルなデータベースマネージャーインスタンス
db_manager = DatabaseManager()