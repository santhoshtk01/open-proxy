import unittest
from src.open_proxy.open_proxy import OpenProxy


class TestOpenProxy(unittest.TestCase):

    def test_check_country(self):
        op = OpenProxy()
        # Valid ISO 3166 country codes.
        for country_code in op.country_list:
            self.assertTrue(op._OpenProxy__check_country(country_code))

    def test_check_protocol(self):
        op = OpenProxy()

        # Valid protocols
        for protocol in ['http', 'socks4', 'socks5']:
            self.assertTrue(op._OpenProxy__check_protocol(protocol))

    def test_anonymity_level(self):
        op = OpenProxy()

        # Valid anonymity levels.
        for anonymity_level in ['elite', 'anonymous', 'transparent']:
            self.assertTrue(op._OpenProxy__check_anonymity_level(anonymity_level))

