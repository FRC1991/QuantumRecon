from BaseHTTPServer import HTTPServer
import SimpleHTTPServer
import re

"""
A simple HTTP server I made a few months ago for another project, based off SimpleHTTPServer (https://docs.python.org/2/library/simplehttpserver.html).
Route methods and error handlers are defined using decorators. Every method is passed a SimpleHTTPRequestHandler which can be used to interact with new requests.
"""

class BottleHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		routes = {regex: func for regex, func in self.server.routes.items() if re.match(regex, self.path)}
		if len(routes) == 0:
			self.throw(404)
			return
		if len(routes) > 1:
			print("WARN: Multiple valid routes for path %s: %s" % (self.path, routes.keys()))
		handler = routes.values()[0]
		handler(self)

	def throw(self, code):
		handler = self.server.handlers.get(code)
		if handler != None:
			handler(self)
		else:
			self.server.default_handle(self, code)

	def respond(self, response, code = 200, mime = "text/plain"):
		self.send_response(code)
		self.send_header("Content-Type", mime)
		self.end_headers()
		self.wfile.write(response)

class Bottle(HTTPServer):
	def __init__(self, port):
		HTTPServer.__init__(self, ("", port), BottleHandler)
		self.routes = {}
		self.handlers = {}

	def route(self, regex):
		def decorator(func):
			print("INFO: Registered '%s' as route for %s" % (func.__name__, regex))
			self.routes[regex] = func
			return func
		return decorator

	def handle(self, code):
		def decorator(func):
			print("INFO: Registered '%s' as handler for status code %s" % (func.__name__, code))
			self.handlers[code] = func
			return func
		return decorator

	def default_handle(self, req, code):
		req.respond("Internal Error", 500)
		print("WARN: No handler to handle status code %s!" % code)
