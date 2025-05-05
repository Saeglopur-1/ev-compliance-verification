# tests/test_data_cleaning.py
from src.data_cleaning import clean_regulation_text

def test_text_cleaning():
    dirty_text = "Article 1  \n  \x0cThis is a \tsample text...\n\n"
    cleaned = clean_regulation_text(dirty_text)
    
    assert "\x0c" not in cleaned  # 控制字符移除
    assert "\t" not in cleaned    # 制表符转换
    assert "  " not in cleaned    # 多余空格
    assert cleaned.startswith("Article 1")  # 结构保留