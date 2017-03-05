from Bottle import Bottle
import girth

port = 8099
server = Bottle(port)

@server.route("\/$")
def index(req): 
	req.respond(open("site/index.html", "r").read(), mime = "text/html")

@server.route("/submit")
def submit(req):
	print req.path
	req.respond("hello men")

try:
	server.serve_forever()
	server.shutdown()
except KeyboardInterrupt:
	pass