import os
import sys
from unittest import TestCase

module_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_dir)
madmac = __import__("madmac")
module = __import__(
    "madmac",
    fromlist=["UnsupportedOperation", "MacGenerator", "handle_args", "main"],
)
UnsupportedOperation = getattr(module, "UnsupportedOperation")
MacGenerator = getattr(module, "MacGenerator")


class TestMadMac(TestCase):
    def test_extract_alphanumeric_case01(self):
        value = madmac.extract_alphanumeric("abc-def")
        self.assertEqual(value, "abcdef")

    def test_extract_alphanumeric_case02(self):
        value = madmac.extract_alphanumeric("abc:def")
        self.assertEqual(value, "abcdef")

    def test_extract_alphanumeric_case03(self):
        value = madmac.extract_alphanumeric("12:34-56")
        self.assertEqual(value, "123456")

    def test_pair_hexvalue(self):
        value = madmac.pair_hexvalue("abcdef", ":")
        self.assertEqual(value, "ab:cd:ef")

    def test_int_to_hexstr(self):
        value = madmac.int_to_hexstr(255)
        self.assertEqual(value, "0000ff")

    def test_int_to_hexstr_ValueError(self):
        self.assertRaises(ValueError, madmac.int_to_hexstr, "255")

    def test_hexstr_to_int(self):
        value = madmac.hexstr_to_int("0000ff")
        self.assertEqual(value, 255)

    def test_access_object_member_case01(self):
        tmp = 1
        value = madmac.access_object_member(tmp, "real")
        self.assertEqual(value, tmp.real)

    def test_access_object_member_case02(self):
        tmp = []
        value = madmac.access_object_member(tmp, "copy")
        self.assertEqual(value, tmp)

    def test_access_object_member_UnsupportedOperation(self):
        tmp = []
        self.assertRaises(
            UnsupportedOperation, madmac.access_object_member, tmp, "get"
        )

    def test_validate_3octets_case01(self):
        tmp = "aabbcc"
        result = madmac.validate_3octets(tmp)
        self.assertTrue(result)

    def test_validate_3octets_case02(self):
        tmp = "123456"
        result = madmac.validate_3octets(tmp)
        self.assertTrue(result)

    def test_validate_3octets_case03(self):
        tmp = 123456
        result = madmac.validate_3octets(tmp)
        self.assertFalse(result)

    def test_validate_3octets_case04(self):
        tmp = "12345"
        result = madmac.validate_3octets(tmp)
        self.assertFalse(result)

    def test_validate_3octets_TypeError(self):
        self.assertFalse(madmac.validate_3octets([]))

    def test_validate_3octets_ValueError(self):
        self.assertFalse(madmac.validate_3octets(""))

    def test_validate_MAC_case01(self):
        self.assertTrue(madmac.validate_mac("12345678912"))

    def test_validate_MAC_case02(self):
        self.assertTrue(madmac.validate_mac("ab-cd-ef-12-34-56"))

    def test_validate_MAC_case03(self):
        self.assertTrue(madmac.validate_mac("ab:cd:ef:12:34:56"))

    def test_validate_MAC_TypeError(self):
        self.assertFalse(madmac.validate_mac("xx:yy:zz"))

    def test_validate_MAC_ValueError(self):
        self.assertFalse(madmac.validate_mac(None))

    def test_mac_generator_prepare_stop_address(self):
        mc = MacGenerator()
        mc._prepare_stop_address()
        self.assertIs(int, type(mc.i_stop))

    def test_mac_generator_prepare_stop_address_user(self):
        mc = MacGenerator(start="000005", stop="000010")
        mc._prepare_stop_address()
        self.assertEqual(16, mc.i_stop)

    def test_mac_generator_prepare_stop_address_ValueError(self):
        mc = MacGenerator(stop="-10")
        self.assertRaises(ValueError, mc._prepare_stop_address)

    def test_mac_generator_prepare_stop_address_user_total(self):
        mc = MacGenerator(total="")
        self.assertRaises(ValueError, mc._prepare_stop_address)

    def test_mac_generator_prepare_stop_address_UnsupportedOperation(self):
        mc = MacGenerator(total="X")
        self.assertRaises(UnsupportedOperation, mc._prepare_stop_address)

    def test_mac_generator_prepare_stop_address_InvalidEndingAddress(self):
        mc = MacGenerator(start="000005", stop="00001G")
        self.assertRaises(ValueError, mc._prepare_stop_address)
