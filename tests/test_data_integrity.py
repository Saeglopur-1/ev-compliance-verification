# tests/test_data_integrity.py
import pytest
from pathlib import Path
import json

@pytest.fixture
def raw_data():
    return Path("data/raw")

@pytest.fixture
def processed_data():
    return Path("data/processed/regulations.json")

def test_raw_files_exist(raw_data):
    """验证原始文件是否下载完整"""
    required_files = {
        "co2_regulation.pdf",
        "battery_regulation.pdf",
        "type_approval_regulation.pdf"
    }
    assert required_files.issubset({f.name for f in raw_data.glob("*.pdf")})

def test_processed_data_structure(processed_data):
    """验证处理后的数据结构"""
    with open(processed_data) as f:
        data = json.load(f)
    
    assert isinstance(data, list)
    for item in data:
        assert "document" in item
        assert "articles" in item
        assert isinstance(item["tables"], list)