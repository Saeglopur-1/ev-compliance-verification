# tests/test_content_integrity.py
import pdfplumber
import re

def test_pdf_text_extraction():
    """验证PDF文本提取完整性"""
    with pdfplumber.open("data/raw/co2_regulation.pdf") as pdf:
        first_page_text = pdf.pages[0].extract_text()
        
        # 关键标志性内容检查
        assert "REGULATION (EU) 2019/631" in first_page_text
        assert "CO2 emissions" in first_page_text
        
        # 检查非乱码字符比例
        non_garbage_ratio = len(re.findall(r'[\w\.,;:]+', first_page_text)) / len(first_page_text.split())
        assert non_garbage_ratio > 0.8