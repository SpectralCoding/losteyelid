#!/usr/bin/env python
"""Executes Shell commands using Windows Remote Management."""

import base64
import uuid
import collections
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
        :returns: A namedtuple containing the stdout and stderr output."""
        decoded = conn_config[3] + ":" + conn_config[4]
        encoded_utf = base64.b64encode(decoded.encode('UTF8'))
        wrm_req = collections.namedtuple(
            'WinRMRequest',
            ['auth', 'path', 'command', 'arguments', 'message_id',
             'shell_id', 'command_id', 'command_output']
        )
        wrm_req.auth = "Basic " + encoded_utf.decode("ascii")
        wrm_req.path = "http://" + str(conn_config[0]) + ":" + \
            str(conn_config[1]) + str(conn_config[2])
        wrm_req.command = command
        wrm_req.arguments = arguments
        wrm_req.message_id = str(uuid.uuid4())
        shell_xml = self.build_shell_request_xml(wrm_req)
        wrm_req.shell_id = self.get_shell(wrm_req, shell_xml)
        command_xml = self.build_command_xml(wrm_req)
        wrm_req.command_id = self.run_command(wrm_req, command_xml)
        command_output = self.receive_all_output(wrm_req)
        delete_xml = self.build_shell_delete_xml(wrm_req)
        self.run_shell_delete(wrm_req, delete_xml)
        return command_output

    def build_shell_request_xml(self, wrm_req):
        """Create a WinRM Shell Request in XML format.

        :param wrm_req: The request object containing relevant request data.
        :returns: An LXML object representing the request xml."""
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.xmlsoap.org/ws/2004/09/transfer/Create",
            wrm_req.message_id
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

    def get_shell(self, wrm_req, shell_xml):
        """Get a ShellID from the given XML.

        :param wrm_req: The request object containing relevant request data.
        :param shell_xml: The xml string to send.
        :returns: The ID of the newly created shell."""
        xml_response = self.send_http(shell_xml, wrm_req)
        response = etree.XML(xml_response)
        return response[1][1][0].text		# TODO: Fix this to be more reliable

    def build_command_xml(self, wrm_req):
        """Create a WinRM Command Run Request in XML format.

        :param wrm_req: The request object containing relevant request data.
        :returns: An LXML object representing the request xml."""
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command",
            wrm_req.message_id
        )
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.SelectorSet(
                ns_w.Selector(wrm_req.shell_id, Name="ShellId")
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
        if wrm_req.arguments:
            cli_properties = [ns_rsp.Command(wrm_req.command), ns_rsp.Arguments(wrm_req.arguments)]
        else:
            cli_properties = [ns_rsp.Command(wrm_req.command)]
        soap_request.append(
            ns_env.Body(
                ns_rsp.CommandLine(
                    *cli_properties
                )
            )
        )
        return soap_request

    def run_command(self, wrm_req, command_xml):
        """Run the Command from the given XML.

        :param wrm_req: The request object containing relevant request data.
        :param command_xml: The xml string to send.
        :returns: The ID of the command just executed."""
        xml_response = self.send_http(command_xml, wrm_req)
        response = etree.XML(xml_response)
        return response[1][0][0].text

    def receive_all_output(self, wrm_req):
        """Repeatedly query the remote host until no more data exists.

        :param wrm_req: The request object containing relevant request data.
        :returns: A tuple containing the stdout and stderr response."""
        command_output = collections.namedtuple(
            'WinRMOutput',
            ['stdout', 'stderr']
        )
        command_output.stdout = ""
        command_output.stderr = ""
        receive_more = True
        while receive_more:
            xml_request = self.build_command_receive_xml(wrm_req)
            xml_resp = self.get_command_output(wrm_req, xml_request)
            for cur_block in xml_resp.iterfind(
                    ".//{http://schemas.microsoft.com/wbem/wsman/1/windows/shell}Stream"):
                if cur_block.text is not None:
                    if cur_block.attrib["Name"].lower() == "stdout":
                        command_output.stdout += base64.b64decode(cur_block.text).decode("ascii")
                    elif cur_block.attrib["Name"].lower() == "stderr":
                        command_output.stderr += base64.b64decode(cur_block.text).decode("ascii")
            receive_more = False		# TODO: Figure out at what point we need to receive more!
        return command_output


    def build_command_receive_xml(self, wrm_req):
        """Create a WinRM Receive Command Response Request in XML format.

        :param wrm_req: The request object containing relevant request data.
        :returns: An LXML object representing the request xml."""
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        ns_env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
        ns_rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive",
            wrm_req.message_id
        )
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.SelectorSet(
                ns_w.Selector(wrm_req.shell_id, Name="ShellId")
            )
        )
        soap_request.append(
            ns_env.Body(
                ns_rsp.Receive(
                    ns_rsp.DesiredStream("stdout stderr", CommandId=wrm_req.command_id)
                )
            )
        )
        return soap_request

    def get_command_output(self, wrm_req, xml_request):
        """Run the Command from the given XML.

        :param wrm_req: The request object containing relevant request data.
        :param xml_request: The xml string to send.
        :returns: An LXML object representing the response xml."""
        xml_response = self.send_http(xml_request, wrm_req)
        return etree.XML(xml_response)

    def build_shell_delete_xml(self, wrm_req):
        """Create a WinRM Shell Delete Request in XML format.

        :param wrm_req: The request object containing relevant request data.
        :returns: An LXML object representing the request xml."""
        soap_request = self.get_soap_header(
            "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
            "http://schemas.xmlsoap.org/ws/2004/09/transfer/Delete",
            wrm_req.message_id
        )
        ns_w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
        ns_env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
        header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
        header_element.append(
            ns_w.SelectorSet(
                ns_w.Selector(wrm_req.shell_id, Name="ShellId")
            )
        )
        soap_request.append(
            ns_env.Body()
        )
        return soap_request

    def run_shell_delete(self, wrm_req, delete_xml):
        """Run the Command from the given XML.

        :param wrm_req: The request object containing relevant request data.
        :param command_xml: The xml string to send.
        :returns: An LXML object representing the response xml."""
        xml_response = self.send_http(delete_xml, wrm_req)
        response = etree.XML(xml_response)
        return response

    @staticmethod
    def send_http(soap_request, wrm_req):
        """Send an XML request to a remote host on a specific path.

        :param soap_request: XML Object representing the data to send.
        :param wrm_req: The request object containing relevant request data.
        :returns: The string response from the server."""
        LOGGER.debug("Outgoing:")
        LOGGER.debug(etree.tostring(soap_request, pretty_print=True).decode("utf-8"))
        soap_str = etree.tostring(soap_request).decode("utf-8")
        ns_r = requests.post(
            wrm_req.path,
            headers={
                "Content-Type": "application/soap+xml;charset=UTF-8",
                "User-Agent": "LostEyelid WinRM Client",
                "Content-Length": len(soap_str),
                "Authorization": wrm_req.auth
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
        :param message_id: The UUID of the related message.
        :returns: An LXML object representing the soap header."""
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
                ns_a.MessageID(message_id),
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
