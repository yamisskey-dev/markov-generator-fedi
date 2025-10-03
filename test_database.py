"""
データベース機能のテスト
"""
import unittest
import os
import tempfile
from database import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    
    def setUp(self):
        """テスト前の準備"""
        # 一時的なデータベースファイルを作成
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_manager = DatabaseManager(self.temp_db.name)
        
        # テスト用のテーブルを作成
        cur = self.db_manager.get_connection().cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS model_data (acct TEXT NOT NULL PRIMARY KEY UNIQUE, data TEXT NOT NULL, allow_generate_by_other INTEGER NOT NULL)')
        cur.close()
        self.db_manager.get_connection().commit()
    
    def tearDown(self):
        """テスト後のクリーンアップ"""
        self.db_manager.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_save_and_get_model_data(self):
        """モデルデータの保存と取得テスト"""
        test_acct = "test@example.com"
        test_data = '{"test": "data"}'
        test_allow = True
        
        # データを保存
        result = self.db_manager.save_model_data(test_acct, test_data, test_allow)
        self.assertTrue(result)
        
        # データを取得
        retrieved_data = self.db_manager.get_model_data(test_acct)
        self.assertIsNotNone(retrieved_data)
        self.assertEqual(retrieved_data['data'], test_data)
    
    def test_model_permissions(self):
        """モデル権限のテスト"""
        test_acct = "test@example.com"
        test_data = '{"test": "data"}'
        
        # 権限ありで保存
        self.db_manager.save_model_data(test_acct, test_data, True)
        permissions = self.db_manager.get_model_permissions(test_acct)
        self.assertIsNotNone(permissions)
        self.assertEqual(permissions['allow_generate_by_other'], 1)
        
        # 権限なしで保存
        self.db_manager.save_model_data(test_acct, test_data, False)
        permissions = self.db_manager.get_model_permissions(test_acct)
        self.assertEqual(permissions['allow_generate_by_other'], 0)
    
    def test_model_exists(self):
        """モデル存在チェックのテスト"""
        test_acct = "test@example.com"
        test_data = '{"test": "data"}'
        
        # 存在しない場合
        self.assertFalse(self.db_manager.model_exists(test_acct))
        
        # 存在する場合
        self.db_manager.save_model_data(test_acct, test_data, True)
        self.assertTrue(self.db_manager.model_exists(test_acct))
    
    def test_delete_model_data(self):
        """モデルデータ削除のテスト"""
        test_acct = "test@example.com"
        test_data = '{"test": "data"}'
        
        # データを保存
        self.db_manager.save_model_data(test_acct, test_data, True)
        self.assertTrue(self.db_manager.model_exists(test_acct))
        
        # データを削除
        result = self.db_manager.delete_model_data(test_acct)
        self.assertTrue(result)
        self.assertFalse(self.db_manager.model_exists(test_acct))


if __name__ == '__main__':
    unittest.main()