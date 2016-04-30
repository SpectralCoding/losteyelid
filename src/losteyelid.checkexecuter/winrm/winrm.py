#!/usr/bin/env python
"""Executes Shell commands using Windows Remote Management."""

import base64
import uuid
import requests
from lxml import etree
from lxml.builder import ElementMaker
import logger

LOGGER = logger.get_logger(__name__)

class WinRM:
    """Executes Shell commands using Windows Remote Management."""

    def __init__(self):
        return

    def run(self, command, arguments, conn_config):
        """Run a shell command remotely with Windown Remote Management.

        :param command: The executable to run.
        :param arguments: The arguments passed to the executable.
        :param conn_config: A list containing the WinRM connection information.
        :returns: None"""
        decoded = conn_config[3] + ":" + conn_config[4]
        encoded_utf = base64.b64encode(decoded.encode('UTF8'))
        auth = "Basic " + encoded_utf.decode("ascii")
        path = "http://" + str(conn_config[0]) + ":" + str(conn_config[1]) + str(conn_config[2])
        message_id = str(uuid.uuid4())
        shell_xml = self.build_shell_request_xml(message_id)
        shell_id = self.get_shell(path, auth, shell_xml)
        command_xml = self.build_command_xml(shell_id, command, arguments, message_id)
        command_id = self.run_command(path, auth, command_xml)
        command_output = {"stdout": "", "stderr": ""}
        receive_more = True
        while receive_more:
            xml_request = self.build_command_receive_xml(shell_id, command_id, message_id)
            xml_resp = self.get_command_output(path, auth, xml_request)
            for cur_block in xml_resp.iterfind(
                    ".//{http://schemas.microsoft.com/wbem/wsman/1/windows/shell}Stream"):
                if cur_block.text is not None:
                    if cur_block.attrib["Name"].lower() == "stdout":
                        command_output["stdout"] += base64.b64decode(cur_block.text).decode("ascii")
                    elif cur_block.attrib["Name"].lower() == "stderr":
                        command_output["stderr"] += base64.b64decode(cur_block.text).decode("ascii")
            LOGGER.debug(command_output)
            receive_more = False		# TODO: Figure out at what point we need to receive more!
        return command_output

    def build_shell_request_xml(self, message_id):
        """Create a WinRM Shell Request in XML format.

        :param message_id: The UUID of the related message.
        :returns: An LXML object representing the request xml."""
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.xmlsoap.org/ws/2004/09/transfer/Create",
            message_id
        )
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        ns_env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
        ns_rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
        soap_request.append(
            ns_env.Body(
                ns_rsp.Shell(
                    ns_rsp.InputStreams("stdin"),
                    ns_rsp.OutputStreams("stderr stdout"),
                )
            )
        )
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.OptionSet(
                ns_w.Option("FALSE", Name="WINRS_NOPROFILE"),
                ns_w.Option("437", Name="WINRS_CODEPAGE")
            )
        )
        return soap_request

    def get_shell(self, path, auth, shell_xml):
        """Get a ShellID from the given XML.

        :param path: The URL path to query.
        :param auth: The Base64 encoded authentication credentials.
        :param shell_xml: The xml string to send."""
        xml_response = self.send_http(shell_xml, path, auth)
        response = etree.XML(xml_response)
        return response[1][1][0].text		# TODO: Fix this to be more reliable

    def build_command_xml(self, shell_id, command, arguments, message_id):
        """Create a WinRM Command Run Request in XML format.

        :param shell_id: The UUID of the related shell.
        :param command: The executable to run.
        :param arguments: The arguments for the executable to run.
        :param message_id: The UUID of the related message.
        :returns: An LXML object representing the request xml."""
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command",
            message_id
        )
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.SelectorSet(
                ns_w.Selector(shell_id, Name="ShellId")
            )
        )
        # TODO: Should the ElementMakers be members?
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.OptionSet(
                ns_w.Option("TRUE", Name="WINRS_CONSOLEMODE_STDIN"),
                ns_w.Option("FALSE", Name="WINRS_SKIP_CMD_SHELL")
            )
        )
        ns_env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
        ns_rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
        if arguments:
            cli_properties = [ns_rsp.Command(command), ns_rsp.Arguments(arguments)]
        else:
            cli_properties = [ns_rsp.Command(command)]
        soap_request.append(
            ns_env.Body(
                ns_rsp.CommandLine(
                    *cli_properties
                )
            )
        )
        return soap_request

    def run_command(self, path, auth, command_xml):
        """Run the Command from the given XML.

        :param path: The URL path to query.
        :param auth: The Base64 encoded authentication credentials.
        :param command_xml: The xml string to send."""
        xml_response = self.send_http(command_xml, path, auth)
        response = etree.XML(xml_response)
        return response[1][0][0].text

    def build_command_receive_xml(self, shell_id, command_id, message_id):
        """Create a WinRM Receive Command Response Request in XML format.

        :param shell_id: The UUID of the related shell.
        :param command_id: The UUID of the related command.
        :param message_id: The UUID of the related message.
        :returns: An LXML object representing the request xml."""
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        ns_env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
        ns_rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive",
            message_id
        )
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.SelectorSet(
                ns_w.Selector(shell_id, Name="ShellId")
            )
        )
        soap_request.append(
            ns_env.Body(
                ns_rsp.Receive(
                    ns_rsp.DesiredStream("stdout stderr", CommandId=command_id)
                )
            )
        )
        return soap_request

    def get_command_output(self, path, auth, xml_request):
        """Run the Command from the given XML.

        :param path: The URL path to query.
        :param auth: The Base64 encoded authentication credentials.
        :param xml_request: The xml string to send."""
        xml_response = self.send_http(xml_request, path, auth)
        return etree.XML(xml_response)

    @staticmethod
    def send_http(soap_request, path, auth):
        """Send an XML request to a remote host on a specific path.

        :param soap_request: XML Object representing the data to send.
        :param path: The URL path to query.
        :param auth: The Base64 encoded authentication credentials."""
        LOGGER.debug("Outgoing:")
        LOGGER.debug(etree.tostring(soap_request, pretty_print=True).decode("utf-8"))
        soap_str = etree.tostring(soap_request).decode("utf-8")
        ns_r = requests.post(
            path,
            headers={
                "Content-Type": "application/soap+xml;charset=UTF-8",
                "User-Agent": "JS WinRM Client",
                "Content-Length": len(soap_str),
                "Authorization": auth
            },
            data=soap_str
        )
        LOGGER.debug("Incoming:")
        LOGGER.debug(ns_r.text)
        return ns_r.text

    @staticmethod
    def get_soap_header(resource_uri, action, message_id):
        """Generates a basic SOAP header to be modified later.

        :param resource_uri: The resource we're working with.
        :param action: The action we're taking.
        :param message_id: The UUID of the related message."""
        env = ElementMaker(
            namespace="http://www.w3.org/2003/05/soap-envelope",
            nsmap={
                "env": "http://www.w3.org/2003/05/soap-envelope",
                "a": "http://schemas.xmlsoap.org/ws/2004/08/addressing",
                "p": "http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd",
                "rsp": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell",
                "w": "http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd",
                "xml": "http://www.w3.org/XML/1998/namespace/"
            }
        )
        ns_a = ElementMaker(namespace="http://schemas.xmlsoap.org/ws/2004/08/addressing")
        ns_p = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd")
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        request = env.Envelope(
            env.Header(
                ns_a.To("http://windows-host:5985/wsman"),
                ns_a.ReplyTo(
                    ns_a.Address(
                        "http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous",
                        **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}
                    )
                ),
                ns_w.MaxEnvelopeSize(
                    "153600",
                    **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
                ns_a.MessageID("uuid:" + message_id),
                ns_w.Locale(
                    **{
                        "{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "false",
                        "{http://www.w3.org/XML/1998/namespace/}lang": "en-US"
                    }
                ),
                ns_p.DataLocale(
                    **{
                        "{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "false",
                        "{http://www.w3.org/XML/1998/namespace/}lang": "en-US"
                    }
                ),
                ns_w.OperationTimeout("PT60.000S"),
                ns_w.ResourceURI(
                    resource_uri,
                    **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
                ns_a.Action(
                    action,
                    **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
            ),
        )
        return request
