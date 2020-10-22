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

    def test_mac_generator(self):
        self.assertIsNotNone(MacGenerator())

    def test_mac_generator_normalize_oui(self):
        mc = MacGenerator(oui="AA:BB:CC", delimiter=" ")
        self.assertEqual(mc.normalize_oui(), "AA BB CC")
        
    def test_mac_generator_pick_random_int(self):
        mc = MacGenerator()
        self.assertIs(int, type(mc._pick_random_int()))

    def test_mac_generator_prepare_oui(self):
        mc = MacGenerator()
        mc._prepare_oui()
        self.assertIs(str, type(mc.oui))

    def test_mac_generator_prepare_oui_user(self):
        mc = MacGenerator(oui="aa:bb:cc")
        mc._prepare_oui()
        self.assertEqual("aabbcc", mc.oui)

    def test_mac_generator_prepare_oui_ValueError(self):
        mc = MacGenerator(oui="xx:yy:zz")
        self.assertRaises(ValueError, mc._prepare_oui)

    def test_mac_generator_prepare_start_address(self):
        mc = MacGenerator()
        mc._prepare_start_address()
        self.assertIs(int, type(mc.i_start))

    def test_mac_generator_prepare_start_address_user(self):
        mc = MacGenerator(start="110000")
        mc._prepare_start_address()
        self.assertEqual(1114112, mc.i_start)

    def test_mac_generator_prepare_start_address_ValueError(self):
        mc = MacGenerator(start="1100YY")
        self.assertRaises(ValueError, mc._prepare_start_address)

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

    def test_mac_generator_validate(self):
        mc = MacGenerator()
        self.assertIsNone(mc._validate())

    def test_mac_generator_build(self):
        mc = MacGenerator()
        mc._validate()
        self.assertIs(str, type(list(mc._build())[-1]))

    def test_mac_generator_generate(self):
        mc = MacGenerator()
        self.assertIs(str, type(list(mc.generate())[-1]))
