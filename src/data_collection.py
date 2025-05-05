import requests
import pdfplumber
from pathlib import Path
import pandas as pd
import logging
from bs4 import BeautifulSoup
import PyPDF2
import io

# 配置日志
logging.basicConfig(filename='data_collection.log', level=logging.INFO)

class RegulationCollector:
    def __init__(self):
        self.reg_sources = {
            "co2": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32019R0631",
            "battery": "https://eur-lex.europa.eu/eli/reg/2023/1542/oj",
            "type_approval": "https://unece.org/transport/documents/2021/02/standards/un-regulation-no-100-rev-3"
        }
        self.raw_data_dir = Path("data/raw")
        self.raw_data_dir.mkdir(exist_ok=True)

    def download_documents(self):
        """下载法规PDF文件"""
        for name, url in self.reg_sources.items():
            try:
                response = requests.get(url, timeout=10)
                output_path = self.raw_data_dir / f"{name}_regulation.pdf"
                output_path.write_bytes(response.content)
                logging.info(f"Downloaded {name} regulation")
            except Exception as e:
                logging.error(f"Failed to download {name}: {str(e)}")

    def extract_text_from_pdf(self):
        """从PDF提取结构化文本（改进版）"""
        processed_data = []
        for pdf_file in self.raw_data_dir.glob("*.pdf"):
            try:
                # 方法1: 使用pdfplumber提取文本（保留原功能）
                with pdfplumber.open(pdf_file) as pdf:
                    text_plumber = "\n".join(page.extract_text() for page in pdf.pages)
                    tables = self._extract_tables(pdf)  # 保留表格提取功能
                
                # 方法2: 使用PyPDF2作为备选方案
                text_pypdf = ""
                with open(pdf_file, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text_pypdf += page.extract_text() + "\n"
                
                # 选择提取效果更好的文本
                text = text_plumber if len(text_plumber) > len(text_pypdf) else text_pypdf
                
                # 提取关键章节
                sections = {
                    "document": pdf_file.stem,
                    "articles": self._extract_articles(text),
                    "tables": tables,
                    "full_text": text[:5000] + "..."  # 保存部分文本作为样例
                }
                processed_data.append(sections)
                
                # 单独保存完整文本
                text_path = self.raw_data_dir / f"{pdf_file.stem}_text.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text)
                    
            except Exception as e:
                logging.error(f"Error processing {pdf_file}: {str(e)}")
        
        # 保存处理结果
        pd.DataFrame(processed_data).to_json("data/processed/regulations.json", indent=2)

    def _extract_articles(self, text: str):
        """提取法规条款（改进版）"""
        import re
        articles = {}
        current_article = None
        
        # 改进的正则表达式，匹配更多格式的条款
        article_pattern = re.compile(r'^(Article|ARTICLE|Art\.?)\s*\d+', re.IGNORECASE)
        
        for line in text.split('\n'):
            line = line.strip()
            if article_pattern.match(line):
                current_article = line
                articles[current_article] = []
            elif current_article:
                if line:  # 忽略空行
                    articles[current_article].append(line)
        
        return {k: '\n'.join(v) for k, v in articles.items()}

    def _extract_tables(self, pdf):
        """提取PDF中的表格数据（改进版）"""
        tables = []
        for page in pdf.pages:
            # 尝试改进表格提取
            table_settings = {
                "vertical_strategy": "text", 
                "horizontal_strategy": "text",
                "intersection_y_tolerance": 10
            }
            for table in page.extract_tables(table_settings):
                cleaned_table = []
                for row in table:
                    cleaned_row = [str(cell).strip() if cell is not None else "" for cell in row]
                    cleaned_table.append(cleaned_row)
                tables.append(cleaned_table)
        return tables

if __name__ == "__main__":
    collector = RegulationCollector()
    collector.download_documents()
    collector.extract_text_from_pdf()