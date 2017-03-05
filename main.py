from Bottle import Bottle
from threading import Thread
import girth, time

port = 8092
server = Bottle(port)

@server.route("\/assets\/.+")
def asset(req):
	file = req.path.split("/")[2]
	try:
		print file
		req.respond(open("assets/%s" % file, "r").read())
	except IOError:
		req.throw(404)


@server.route("\/$")
def index(req): 
	req.respond(open("site/index.html", "r").read(), mime = "text/html")

@server.route("\/submit\?line=(\d+,)+")
def submit(req):
	print path
	req.respond("hello men")

try:
	server.serve_forever()
	server.shutdown()
except KeyboardInterrupt:
	pass