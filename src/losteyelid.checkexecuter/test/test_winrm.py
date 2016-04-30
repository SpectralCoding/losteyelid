#!/usr/bin/env python
"""Tests the WinRM module."""

import unittest
from lxml import etree
from winrm.winrm import WinRM

class WinRMTest(unittest.TestCase):
    """Tests the WinRM module."""
    maxDiff = None

    @unittest.skip("Not a good test candidate.")
    def test_run(self):
        """Tests WinRM.run()."""

    def test_build_shell_request_xml(self):
        """Tests WinRM.build_shell_request_xml()."""
        winrm = WinRM()
        xml_obj = winrm.build_shell_request_xml("SAMPLE-MESSAGE-ID")
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>uuid:SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
        self.assertTrue('<w:OperationTimeout>PT60.000S</w:OperationTimeout>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">'
                        'http://schemas.xmlsoap.org/ws/2004/09/transfer/Create'
                        '</a:Action>' in xml_str)
        self.assertTrue('<w:Option Name="WINRS_NOPROFILE">FALSE</w:Option>' in xml_str)
        self.assertTrue('<w:Option Name="WINRS_CODEPAGE">437</w:Option>' in xml_str)
        self.assertTrue('<rsp:InputStreams>stdin</rsp:InputStreams>' in xml_str)
        self.assertTrue('<rsp:OutputStreams>stderr stdout</rsp:OutputStreams>' in xml_str)

    @unittest.skip("Not a good test candidate.")
    def test_get_shell(self):
        """Tests WinRM.get_shell()."""

    def test_build_command_xml(self):
        """Tests WinRM.build_command_xml()."""
        winrm = WinRM()
        xml_obj = winrm.build_command_xml("SAMPLE-SHELL-ID",
                                          "SAMPLE-COMMAND",
                                          "SAMPLE-ARGUMENTS",
                                          "SAMPLE-MESSAGE-ID")
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>uuid:SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
        self.assertTrue('<w:OperationTimeout>PT60.000S</w:OperationTimeout>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command'
                        '</a:Action>' in xml_str)
        self.assertTrue('<w:Selector Name="ShellId">SAMPLE-SHELL-ID</w:Selector>' in xml_str)
        self.assertTrue('<w:Option Name="WINRS_CONSOLEMODE_STDIN">TRUE</w:Option>' in xml_str)
        self.assertTrue('<rsp:Command>SAMPLE-COMMAND</rsp:Command>' in xml_str)
        self.assertTrue('<rsp:Arguments>SAMPLE-ARGUMENTS</rsp:Arguments>' in xml_str)

    @unittest.skip("Not a good test candidate.")
    def test_run_command(self):
        """Tests WinRM.run_command()."""

    def test_build_command_receive_xml(self):
        """Tests WinRM.build_command_receive_xml()."""
        winrm = WinRM()
        xml_obj = winrm.build_command_receive_xml("SAMPLE-SHELL-ID",
                                                  "SAMPLE-COMMAND-ID",
                                                  "SAMPLE-MESSAGE-ID")
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>uuid:SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
        self.assertTrue('<w:OperationTimeout>PT60.000S</w:OperationTimeout>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive'
                        '</a:Action>' in xml_str)
        self.assertTrue('<w:Selector Name="ShellId">SAMPLE-SHELL-ID</w:Selector>' in xml_str)
        self.assertTrue('<rsp:DesiredStream CommandId="SAMPLE-COMMAND-ID">'
                        'stdout stderr'
                        '</rsp:DesiredStream>' in xml_str)

    @unittest.skip("Not a good test candidate.")
    def test_get_command_output(self):
        """Tests WinRM.get_command_output()."""

    @unittest.skip("Not a good test candidate.")
    def test_send_http(self):
        """Tests WinRM.send_http()."""

    def test_get_soap_header(self):
        """Tests WinRM.get_soap_header()."""
        winrm = WinRM()
        xml_obj = winrm.get_soap_header("SAMPLE-RESOURCE-URI", "SAMPLE-ACTION", "SAMPLE-UUID")
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>uuid:SAMPLE-UUID</a:MessageID>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'SAMPLE-RESOURCE-URI'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">SAMPLE-ACTION</a:Action>' in xml_str)

if __name__ == '__main__':
    unittest.main()
