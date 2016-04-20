import logger
import base64
import uuid
import requests
from lxml import etree
from lxml.builder import ElementMaker

logger = logger.get_logger(__name__)

class WinRM:

	def __init__(self):
		return

	def run(self, command, arguments, conn_config):
		decoded = conn_config[3] + ":" + conn_config[4]
		encoded_utf = base64.b64encode(decoded.encode('UTF8'))
		auth = "Basic " + encoded_utf.decode("ascii")
		path = "http://" + str(conn_config[0]) + ":" + str(conn_config[1]) + str(conn_config[2])
		message_id = str(uuid.uuid4())
		shell_id = self.get_shell(path, auth, message_id)
		command_id = self.run_command(shell_id, command, arguments, path, auth, message_id)
		command_output = { "stdout": "", "stderr": "" }
		receive_more = True
		while receive_more:
			xml_resp = self.get_command_output(shell_id, command_id, path, auth, message_id)
			for cur_block in xml_resp.iterfind(".//{http://schemas.microsoft.com/wbem/wsman/1/windows/shell}Stream"):
				if cur_block.text is not None:
					if cur_block.attrib["Name"].lower() == "stdout":
						command_output["stdout"] += base64.b64decode(cur_block.text).decode("ascii")
					elif cur_block.attrib["Name"].lower() == "stderr":
						command_output["stderr"] += base64.b64decode(cur_block.text).decode("ascii")
			logger.debug(command_output)
			receive_more = False		# TODO: Figure out at what point we need to receive more!
		return command_output

	def get_shell(self, path, auth, message_id):
		soap_request = self.get_soap_header(
			"http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"http://schemas.xmlsoap.org/ws/2004/09/transfer/Create",
			message_id
		)
		w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
		env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
		rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
		soap_request.append(
			env.Body(
				rsp.Shell(
					rsp.InputStreams("stdin"),
					rsp.OutputStreams("stderr stdout"),
				)
			)
		)
		header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
		header_element.append(
			w.OptionSet(
				w.Option("FALSE", Name="WINRS_NOPROFILE"),
				w.Option("437", Name="WINRS_CODEPAGE")
			)
		)
		xml_response = self.send_http(soap_request, path, auth)
		response = etree.XML(xml_response)
		return response[1][1][0].text		# TODO: Fix this to be more reliable

	def get_command_output(self, shell_id, command_id, path, auth, message_id):
		w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
		env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
		rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
		soap_request = self.get_soap_header(
			"http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive",
			message_id
		)
		header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
		header_element.append(
			w.SelectorSet(
				w.Selector(shell_id, Name="ShellId")
			)
		)
		soap_request.append(
			env.Body(
				rsp.Receive(
					rsp.DesiredStream("stdout stderr", CommandId=command_id)
				)
			)
		)
		xml_response = self.send_http(soap_request, path, auth)
		return etree.XML(xml_response)

	def run_command(self, shell_id, command, arguments, path, auth, message_id):
		soap_request = self.get_soap_header(
			"http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command",
			message_id
		)
		w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
		header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
		header_element.append(
			w.SelectorSet(
				w.Selector(shell_id, Name="ShellId")
			)
		)
		# TODO: Should the ElementMakers be members?
		header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
		header_element.append(
			w.OptionSet(
				w.Option("TRUE", Name="WINRS_CONSOLEMODE_STDIN"),
				w.Option("FALSE", Name="WINRS_SKIP_CMD_SHELL")
			)
		)
		env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
		rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
		if arguments:
			cli_properties = [rsp.Command(command), rsp.Arguments(arguments)]
		else:
			cli_properties = [rsp.Command(command)]
		soap_request.append(
			env.Body(
				rsp.CommandLine(
					*cli_properties
				)
			)
		)

		xml_response = self.send_http(soap_request, path, auth)
		response = etree.XML(xml_response)
		return response[1][0][0].text

	def send_http(self, soap_request, path, auth):
		logger.debug("Outgoing:")
		logger.debug(etree.tostring(soap_request, pretty_print=True).decode("utf-8"))
		soap_str = etree.tostring(soap_request).decode("utf-8")
		r = requests.post(
			path,
			headers={
				"Content-Type": "application/soap+xml;charset=UTF-8",
				"User-Agent": "JS WinRM Client",
				"Content-Length": len(soap_str),
				"Authorization": auth
			},
			data=soap_str
		)
		logger.debug("Incoming:")
		logger.debug(r.text)
		return r.text

	def get_soap_header(self, resource_uri, action, message_id):
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
		a = ElementMaker(namespace="http://schemas.xmlsoap.org/ws/2004/08/addressing")
		p = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/wsman.xsd")
		w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
		request = env.Envelope(
			env.Header(
				a.To("http://windows-host:5985/wsman"),
				a.ReplyTo(
					a.Address(
						"http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous",
						**{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}
					)
				),
				w.MaxEnvelopeSize("153600", **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
				a.MessageID("uuid:" + message_id),
				w.Locale(
					**{
						"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "false",
						"{http://www.w3.org/XML/1998/namespace/}lang": "en-US"
					}
				),
				p.DataLocale(
					**{
						"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "false",
						"{http://www.w3.org/XML/1998/namespace/}lang": "en-US"
					}
				),
				w.OperationTimeout("PT60.000S"),
				w.ResourceURI(resource_uri, **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
				a.Action(action, **{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}),
			),
		)
		return request
