import unittest
import unittest.mock
import os

import bb_parser


class TestParseBitBakeFile(unittest.TestCase):
    def test_scrape_version_htop(self):
        """"
        Test that the version is correctly scraped from the file name
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        expect = "1.0.3"
        self.assertEqual(expect, bb_parser.scrape_version(os.path.basename(bb_file)))

    def test_scrape_version_vim(self):
        """"
        Test that the version is correctly scraped from the file name
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        expect = "8.0.0983"
        self.assertEqual(expect, bb_parser.scrape_version(os.path.basename(bb_file)))

    def test_scrape_inherits_htop(self):
        """
        Test that the package inherits are correctly scraped as a list with
        only one line/inherit
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = ["autotools"]
        self.assertEqual(expect, bb_dict.get('inherits'))

    def test_scrape_inherits_vim(self):
        """
        Test that the package inherits are correctly scraped as a list with
        multiple lines/inherits
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = ["autotools update-alternatives", "autotools-brokensep"]
        self.assertEqual(expect, bb_dict.get('inherits'))

if __name__ == '__main__':
    unittest.main(buffer=True)
