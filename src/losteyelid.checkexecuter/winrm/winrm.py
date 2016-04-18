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

	def run(self, command, host, port, path, username, password):
		run_params = {
			"resource_uri": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"action": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command",
			"shell_id": '',
			"command": command,
			"host": host,
			"port": port,
			"path": "http://" + str(host) + ":" + str(port) + str(path),
			"username": username,
			"password": password,
			"auth": None,
			"shell_id": None,
			"command_id": None,
			"results": None
		}
		decoded = username + ":" + password
		encoded_utf = base64.b64encode(decoded.encode('UTF8'))
		run_params["auth"] = "Basic " + encoded_utf.decode("ascii")
		run_params["shell_id"] = self.open_shell(run_params)
		run_params["command_id"] = self.run_command(run_params)
		self.get_command_output(run_params)
		return

	def open_shell(self, run_params):
		soap_request = self.get_soap_header({
			"resource_uri": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"action": "http://schemas.xmlsoap.org/ws/2004/09/transfer/Create"
		})
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
		xml_response = self.send_http(soap_request, run_params)
		response = etree.XML(xml_response)
		#shell_id = response.findall("{http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd}Selector")
		return response[1][1][0].text		# TODO: Fix this to be more reliable

	def get_command_output(self, run_params):
		soap_request = self.get_soap_header({
			"resource_uri": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"action": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Receive",
			"shell_id": run_params['shell_id']
		})
		env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
		rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
		soap_request.append(
			env.Body(
				rsp.Receive(
					rsp.DesiredStream("stdout stderr", CommandId=run_params["command_id"])
				)
			)
		)
		xml_response = self.send_http(soap_request, run_params)
		response = etree.XML(xml_response)
		raw_response = response[1][0][1].text
		logger.debug(base64.b64decode(raw_response).decode("ascii"))
		#return response[1][0][0].text
		return


	def run_command(self, run_params):
		soap_request = self.get_soap_header({
			"resource_uri": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/cmd",
			"action": "http://schemas.microsoft.com/wbem/wsman/1/windows/shell/Command",
			"shell_id": run_params['shell_id']
		})
		# TODO: Should the ElementMakers be members?
		w = ElementMaker(namespace="http://schemas.dmtf.org/wbem/wsman/1/wsman.xsd")
		header_element = soap_request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
		header_element.append(
			w.OptionSet(
				w.Option("TRUE", Name="WINRS_CONSOLEMODE_STDIN"),
				w.Option("FALSE", Name="WINRS_SKIP_CMD_SHELL")
			)
		)
		env = ElementMaker(namespace="http://www.w3.org/2003/05/soap-envelope")
		rsp = ElementMaker(namespace="http://schemas.microsoft.com/wbem/wsman/1/windows/shell")
		soap_request.append(
			env.Body(
				rsp.CommandLine(
					rsp.Command(run_params["command"])
				)
			)
		)
		xml_response = self.send_http(soap_request, run_params)
		response = etree.XML(xml_response)
		return response[1][0][0].text

	def send_http(self, soap_request, run_params):
		logger.debug(etree.tostring(soap_request, pretty_print=True).decode("utf-8"))
		soap_str = etree.tostring(soap_request).decode("utf-8")
		r = requests.post(
			run_params["path"],
			headers={
				"Content-Type": "application/soap+xml;charset=UTF-8",
				"User-Agent": "JS WinRM Client",
				"Content-Length": len(soap_str),
				"Authorization": run_params["auth"]
			},
			data=soap_str
		)
		logger.debug(r.text)
		return r.text

	def get_soap_header(self, run_params):
		if "message_id" not in run_params or run_params["message_id"] is None:
			run_params["message_id"] = str(uuid.uuid4())
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
				w.MaxEnvelopeSize(
					"153600",
					**{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}
				),
				a.MessageID("uuid:" + run_params["message_id"]),
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
				w.ResourceURI(
					run_params["resource_uri"],  # Swap this later
					**{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}
				),
				a.Action(
					run_params["action"],  # Swap this later
					**{"{http://www.w3.org/2003/05/soap-envelope}mustUnderstand": "true"}
				),
			),
		)
		if "shell_id" in run_params and run_params["shell_id"] is not None:
			header_element = request.find("{http://www.w3.org/2003/05/soap-envelope}Header")
			header_element.append(
				w.SelectorSet(
					w.Selector(run_params["shell_id"], Name="ShellId")
				)
			)
		return request
