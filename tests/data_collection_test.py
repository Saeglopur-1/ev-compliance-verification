import pytest
from src.data_collection import RegulationCollector
from unittest.mock import patch, Mock
from pathlib import Path 

class TestRegulationCollector:
    @patch('requests.get')
    def test_download_documents(self, mock_get):
        mock_response = Mock()
        mock_response.content = b"PDF content"
        mock_get.return_value = mock_response

        collector = RegulationCollector()
        collector.download_documents()
        
        assert (collector.raw_data_dir / "co2_regulation.pdf").exists()
    
    @patch('pdfplumber.open')
    def test_extract_text(self, mock_pdf):
        mock_page = Mock()
        mock_page.extract_text.return_value = "Sample text"
        mock_pdf.return_value.pages = [mock_page]

        collector = RegulationCollector()
        collector.extract_text_from_pdf()
        
        output_file = Path("data/processed/regulations.json")
        assert output_file.exists()