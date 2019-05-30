from unittest import TestCase


import madmac


class TestMadMac(TestCase):

    def test_format_hexstr(self):
        value = madmac.format_hexstr('abcdef', ':')
        self.assertEqual(value, 'ab:cd:ef')

    def test_int_to_hexstr(self):
        value = madmac.int_to_hexstr(255)
        self.assertEqual(value, '0000ff')

    def test_hexstr_to_int(self):
        value = madmac.hexstr_to_int('0000ff')
        self.assertEqual(value, 255)

    def test_normalize_oui(self):
        value = madmac.normalize_oui('aa-bb-cc', delimiter=':')
        self.assertEqual(value, 'aa:bb:cc')

