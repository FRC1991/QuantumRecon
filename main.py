from Bottle import Bottle
from threading import Thread
import girth, time, urllib

port = 8080
server = Bottle(port)

@server.route("\/assets\/.+")
def asset(req):
	file = req.path.split("/")[2]
	try:
		req.respond(open("assets/%s" % file, "r").read())
	except IOError:
		req.throw(404)


@server.route("\/$")
def index(req): 
	req.respond(open("site/index.html", "r").read(), mime = "text/html")

@server.route("\/submit\?line=(\d+,)+")
def submit(req):
	line = urllib.unquote(req.path[13:])
	output = girth.excellInputer(line)
	if output == True:
		req.respond("yessssss")
	else:
		req.respond(output, code = 500)

try:
	server.serve_forever()
	server.shutdown()
except KeyboardInterrupt:
	pass