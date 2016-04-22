import unittest
from lxml import etree
from winrm.winrm import WinRM

class WinRMTest(unittest.TestCase):
    maxDiff = None

    @unittest.skip("Not a good test candidate.")
    def test_run(self):
        self.assertTrue(True)

    @unittest.skip("Not a good test candidate.")
    def test_get_shell(self):
        self.assertTrue(True)

    @unittest.skip("Not a good test candidate.")
    def test_get_command_output(self):
        self.assertTrue(True)

    @unittest.skip("Not a good test candidate.")
    def test_run_command(self):
        self.assertTrue(True)

    @unittest.skip("Not a good test candidate.")
    def test_send_http(self):
        self.assertTrue(True)

    def test_get_soap_header(self):
        winrm = WinRM()
        soap_header = winrm.get_soap_header("SAMPLE-RESOURCE-URI-HERE", "SAMPLE-ACTION-HERE", "SAMPLE-UUID-HERE")
        soap_header_string = etree.tostring(soap_header).decode("utf-8")
        self.assertTrue('<a:MessageID>uuid:SAMPLE-UUID-HERE</a:MessageID>' in soap_header_string)
        self.assertTrue(
            '<w:ResourceURI env:mustUnderstand="true">SAMPLE-RESOURCE-URI-HERE</w:ResourceURI>' in soap_header_string
        )
        self.assertTrue('<a:Action env:mustUnderstand="true">SAMPLE-ACTION-HERE</a:Action>' in soap_header_string)

    if __name__ == '__main__':
        unittest.main()
