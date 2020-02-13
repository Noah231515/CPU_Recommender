from django.test import TestCase
from utils.passmark_scraper.scraper import PassmarkScraper 

# Create your tests here.
class WebscraperTestCases(TestCase):
    def setUp(self):
        return super().setUp()

    def test_1(self):
        print("made it to test 1")
        scraper = PassmarkScraper('gpu')
        scraped_data = scraper.get_data()
        print(f'Scraped Data:{scraped_data}')