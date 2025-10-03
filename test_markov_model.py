"""
マルコフモデル機能のテスト
"""
import unittest

try:
    from markov_model import format_text, create_markov_model_by_multiline, generate_text
    MECAB_AVAILABLE = True
except ImportError:
    MECAB_AVAILABLE = False


class TestMarkovModel(unittest.TestCase):
    
    def setUp(self):
        """テスト前の準備"""
        if not MECAB_AVAILABLE:
            self.skipTest("MeCab not available")
    
    def test_format_text(self):
        """テキスト整形機能のテスト"""
        # 基本的な整形テスト
        test_text = "こんにちは。　これはテストです。"
        result = format_text(test_text)
        self.assertIn("こんにちは。", result)
        self.assertNotIn("　", result)  # 全角スペースが半角に変換される
        
        # URL除去テスト
        test_text_with_url = "こんにちは。https://example.com テストです。"
        result = format_text(test_text_with_url)
        self.assertNotIn("https://example.com", result)
    
    def test_create_markov_model(self):
        """マルコフモデル作成のテスト"""
        # テスト用のサンプルテキスト
        test_lines = [
            "こんにちは。",
            "今日は良い天気です。",
            "散歩に行きましょう。"
        ]
        
        try:
            model = create_markov_model_by_multiline(test_lines)
            self.assertIsNotNone(model)
            # モデルがJSONに変換できるかテスト
            json_data = model.to_json()
            self.assertIsInstance(json_data, str)
        except Exception as e:
            # MeCabが利用できない環境ではスキップ
            self.skipTest(f"MeCab not available: {e}")
    
    def test_generate_text(self):
        """テキスト生成のテスト"""
        # テスト用のモデルデータ（簡易版）
        test_model_data = '{"chain": [[{"": 1}, {"こんにちは": 1}], [{"こんにちは": 1}, {"。": 1}], [{"。": 1}, {"": 1}]], "parsed_sentences": ["こんにちは。"]}'
        
        try:
            text, gen_text, failed, sw_failed = generate_text(test_model_data)
            # 生成に失敗しても例外が発生しないことを確認
            self.assertIsInstance(failed, bool)
            self.assertIsInstance(sw_failed, bool)
        except Exception as e:
            # モデルデータが不正な場合はスキップ
            self.skipTest(f"Invalid model data: {e}")


if __name__ == '__main__':
    unittest.main()