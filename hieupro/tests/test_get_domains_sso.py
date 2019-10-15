import unittest
from hieupro.models.sso.sso_register import SSORegister


class MyTestCase(unittest.TestCase):

    def test_get_domains_sso(self):
        records = SSORegister.get_domains('kuriboh')
        self.assertEqual(True if records else False, False)
        new_records = [x[0] for x in records]
        self.assertEqual(type(new_records) is list, True)

