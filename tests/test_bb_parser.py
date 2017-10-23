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

    def test_scrape_summary_htop(self):
        """
        Test that the package summary is correctly scraped
        from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "htop process monitor"
        self.assertEqual(expect, bb_dict.get('SUMMARY'))

    def test_scrape_section_htop(self):
        """
        Test that the package section is correctly scraped
        from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "console/utils"
        self.assertEqual(expect, bb_dict.get('SECTION'))

    def test_scrape_license_htop(self):
        """
        Test that the package license is correctly scraped
        from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "GPLv2"
        self.assertEqual(expect, bb_dict.get('LICENSE'))

    def test_scrape_depends_htop(self):
        """
        Test that the package depends is correctly scraped
        from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "ncurses"
        self.assertEqual(expect, bb_dict.get('DEPENDS'))

    def test_scrape_rdepends_htop(self):
        """
        Test that the package rsuggests_${PN} is correctly scraped
        from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "ncurses-terminfo"
        self.assertEqual(expect, bb_dict.get('RDEPENDS_${PN}'))

    def test_scrape_lic_files_chksum_htop_double_eq(self):
        """
        Test that the package license file checksum is correctly scraped
        from the bitbake file. This line contains two equal signs - which
        will test pattern matching identifies the correct one.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'htop_1.0.3.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "file://COPYING;md5=c312653532e8e669f30e5ec8bdc23be3"
        self.assertEqual(expect, bb_dict.get('LIC_FILES_CHKSUM'))

    def test_scrape_s_variable_vim(self):
        """
        Test that the s variable is correctly scraped from the bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "${WORKDIR}/git/src"
        self.assertEqual(expect, bb_dict.get('S'))

    def test_scrape_vimdir_vim(self):
        """
        Test that the vimdir variable is correctly scraped from the bitbake
        file. This value contains multile 'PV' variables.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "vim${@d.getVar('PV').split('.')[0]}${@d.getVar('PV').split('.')[1]}"
        self.assertEqual(expect, bb_dict.get('VIMDIR'))

    def test_scrape_packageconfig_gtkgui_vim(self):
        """
        Test that packageconfig[gtkgui] returns the correct value scraped with
        the parser.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "--enable-gtk2-test --enable-gui=gtk2,--enable-gui=no,gtk+,"
        self.assertEqual(expect, bb_dict.get('PACKAGECONFIG[gtkgui]'))

    def test_scrape_packageconfig_tiny_vim(self):
        """
        Test that packageconfig[tiny] returns the correct value scraped with
        the parser.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "--with-features=tiny,--with-features=big,,"
        self.assertEqual(expect, bb_dict.get('PACKAGECONFIG[tiny]'))

    def test_scrape_alternative_link_name_vim(self):
        """
        Test that ALTERNATIVE_LINK_NAME[vim] is correctly scraped from the
        bitbake file.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "${bindir}/vim"
        self.assertEqual(expect, bb_dict.get('ALTERNATIVE_LINK_NAME[vim]'))

    def test_scrape_files_tutor_has_hyphen_vim(self):
        """
        Test that FILES_${PN}-tutor is correctly scraped. It contains a hyphen
        in the variable name.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "${datadir}/${BPN}/${VIMDIR}/tutor ${bindir}/${BPN}tutor"
        self.assertEqual(expect, bb_dict.get('FILES_${PN}-tutor'))

    def test_scrape_packageconfig_x11_has_digits_vim(self):
        """
        Test that PACKAGECONFIG[x11] is correctly scraped. It contains digits
        in the variable name.
        """
        bb_file = os.path.join('tests', 'testfiles', 'bb', 'vim_8.0.0983.bb')
        bb_dict = bb_parser.bb_scraper(bb_file, None)
        expect = "--with-x,--without-x,xt,"
        self.assertEqual(expect, bb_dict.get('PACKAGECONFIG[x11]'))


if __name__ == '__main__':
    unittest.main(buffer=True)
