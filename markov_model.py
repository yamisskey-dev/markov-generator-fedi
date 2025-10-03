"""
マルコフモデルの作成と管理を行うモジュール
"""
import re
import MeCab
import markovify
import config
from typing import List


def format_text(text: str) -> str:
    """テキストを整形する"""
    text = text.replace('　', ' ')  # Full width spaces
    text = re.sub(r'(.+。) (.+。)', r'\1 \2\n', text)
    text = re.sub(r'\n +', '\n', text)  # Spaces
    text = re.sub(r'([。．！？…])\n」', r'\1」 \n', text)  # \n before 」
    text = re.sub(r'\n +', '\n', text)  # Spaces
    text = re.sub(r'\n+', r'\n', text).rstrip('\n')  # Empty lines
    text = re.sub(r'\n +', '\n', text)  # Spaces
    text = re.sub(r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', '', text)  # URL
    return text


def create_markov_model_by_multiline(lines: List[str]):
    """複数行のテキストからマルコフモデルを作成"""
    # MeCabで形態素解析
    parsed_text = []
    mecab_options = ['-Owakati']
    
    try:
        if getattr(config, 'MECAB_DICDIR'):
            mecab_options.append(f'-d{config.MECAB_DICDIR}')
    except AttributeError:
        pass

    try:
        if getattr(config, 'MECAB_RC'):
            mecab_options.append(f'-r{config.MECAB_RC}')
    except AttributeError:
        pass
    
    for line in lines:
        parsed_text.append(MeCab.Tagger(' '.join(mecab_options)).parse(line))
    
    # モデル作成
    try:
        text_model = markovify.NewlineText('\n'.join(parsed_text), state_size=2)
    except Exception as e:
        print(f"Markov model creation failed: {e}")
        raise Exception('<meta name="viewport" content="width=device-width">モデル作成に失敗しました。学習に必要な投稿数が不足している可能性があります。', 500)

    return text_model


def generate_text(model_data: str, min_words: int = 1, startswith: str = '') -> tuple:
    """マルコフモデルからテキストを生成"""
    text_model = markovify.Text.from_json(model_data)
    markov_params = dict(
        tries=100,
        min_words=min_words
    )

    loop_count = 1
    sw_failed = False
    if startswith:
        loop_count = 256

    try:
        if startswith:
            gen_text = text_model.make_sentence_with_start(startswith, **markov_params)
        else:
            gen_text = text_model.make_sentence(**markov_params)
        
        if gen_text:
            text = gen_text.replace(' ', '')
            return text, gen_text, False, False
        else:
            return None, None, True, False
            
    except AttributeError:
        return None, None, True, False
    except markovify.text.ParamError:
        return None, None, True, True if startswith else False
    except KeyError:
        return None, None, True, True if startswith else False