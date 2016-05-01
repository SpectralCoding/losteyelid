#!/usr/bin/env python
"""Tests the WinRM module."""

import collections
import unittest
from lxml import etree
from winrm.winrm import WinRM

class WinRMTest(unittest.TestCase):
    """Tests the WinRM module."""

    @unittest.skip("Not a good test candidate.")
    def test_run(self):
        """Tests WinRM.run()."""

    def test_build_shell_request_xml(self):
        """Tests WinRM.build_shell_request_xml()."""
        winrm = WinRM()
        wrm_req = collections.namedtuple('Request', ['message_id'])
        wrm_req.message_id = "SAMPLE-MESSAGE-ID"
        xml_obj = winrm.build_shell_request_xml(wrm_req)
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
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
        wrm_req = collections.namedtuple(
            'Request',
            ['command', 'arguments', 'message_id', 'shell_id']
        )
        wrm_req.message_id = "SAMPLE-MESSAGE-ID"
        wrm_req.shell_id = "SAMPLE-SHELL-ID"
        wrm_req.command = "SAMPLE-COMMAND"
        wrm_req.arguments = "SAMPLE-ARGUMENTS"
        xml_obj = winrm.build_command_xml(wrm_req)
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
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

    @unittest.skip("Not a good test candidate.")
    def test_receive_all_output(self):
        """Tests WinRM.receive_all_output()."""

    def test_build_command_receive_xml(self):
        """Tests WinRM.build_command_receive_xml()."""
        winrm = WinRM()
        wrm_req = collections.namedtuple(
            'Request',
            ['message_id', 'shell_id', 'command_id']
        )
        wrm_req.message_id = "SAMPLE-MESSAGE-ID"
        wrm_req.shell_id = "SAMPLE-SHELL-ID"
        wrm_req.command_id = "SAMPLE-COMMAND-ID"
        xml_obj = winrm.build_command_receive_xml(wrm_req)
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
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

    def test_build_shell_delete_xml(self):
        """Tests WinRM.build_shell_delete_xml()."""
        winrm = WinRM()
        wrm_req = collections.namedtuple('Request', ['message_id', 'shell_id'])
        wrm_req.message_id = "SAMPLE-MESSAGE-ID"
        wrm_req.shell_id = "SAMPLE-SHELL-ID"
        xml_obj = winrm.build_shell_delete_xml(wrm_req)
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>SAMPLE-MESSAGE-ID</a:MessageID>' in xml_str)
        self.assertTrue('<w:OperationTimeout>PT60.000S</w:OperationTimeout>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">'
                        'http://schemas.xmlsoap.org/ws/2004/09/transfer/Delete'
                        '</a:Action>' in xml_str)
        self.assertTrue('<w:Selector Name="ShellId">SAMPLE-SHELL-ID</w:Selector>' in xml_str)
        self.assertTrue('<env:Body' in xml_str)

    @unittest.skip("Not a good test candidate.")
    def test_run_shell_delete(self):
        """Tests WinRM.run_shell_delete()."""

    @unittest.skip("Not a good test candidate.")
    def test_send_http(self):
        """Tests WinRM.send_http()."""

    def test_get_soap_header(self):
        """Tests WinRM.get_soap_header()."""
        winrm = WinRM()
        xml_obj = winrm.get_soap_header("SAMPLE-RESOURCE-URI", "SAMPLE-ACTION", "SAMPLE-UUID")
        xml_str = etree.tostring(xml_obj).decode("utf-8")
        self.assertTrue('<a:MessageID>SAMPLE-UUID</a:MessageID>' in xml_str)
        self.assertTrue('<w:ResourceURI env:mustUnderstand="true">'
                        'SAMPLE-RESOURCE-URI'
                        '</w:ResourceURI>' in xml_str)
        self.assertTrue('<a:Action env:mustUnderstand="true">SAMPLE-ACTION</a:Action>' in xml_str)

if __name__ == '__main__':
    unittest.main()
