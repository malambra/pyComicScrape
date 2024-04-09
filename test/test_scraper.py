import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from src import scraper

class MockSoupElement:
    def __init__(self, text):
        self.text = text
        self.attrs = {"content": text}

    def __getitem__(self, item):
        return self.attrs[item]

    def get_text(self, strip=False):
        return self.text.strip() if strip else self.text

class TestScraper(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    def test_parse_args(self, mock_args):
        mock_args.return_value = MagicMock(page_type='comics', page_id='123', debug=False)
        args = scraper.parse_args()
        self.assertEqual(args.page_type, 'comics')
        self.assertEqual(args.page_id, '123')
        self.assertEqual(args.debug, False)

    @patch('requests.get')
    def test_fetch_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = "<html></html>"
        mock_get.return_value = mock_response
        soup = scraper.fetch_page('http://example.com')
        self.assertIsInstance(soup, BeautifulSoup)

    @patch('requests.get')
    def test_fetch_page_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        soup = scraper.fetch_page('http://example.com')
        self.assertIsNone(soup)


    @patch('pymongo.collection.Collection.insert_one')
    def test_insert_data(self, mock_insert_one):
        mock_insert_one.return_value = MagicMock(acknowledged=True)
        scraper.insert_data(MagicMock(), {}, False)

    @patch('bs4.BeautifulSoup.find')
    @patch('bs4.BeautifulSoup.select_one')
    @patch('bs4.BeautifulSoup.select')
    def test_scrape_page(self, mock_select, mock_select_one, mock_find):
        soup = BeautifulSoup("<html></html>", "html.parser")
        mock_find.return_value = MockSoupElement("test")
        mock_select_one.return_value = MockSoupElement("3.5")
        mock_select.return_value = [MockSoupElement("test")]
        data = scraper.scrape_page(soup, 'comics', 'http://example.com/123')
        self.assertEqual(data["Descripcion"], "test")

if __name__ == '__main__':
    unittest.main()