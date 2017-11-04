from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endwith("/hello"):
				self.send_response(200)
				self.send_header('Content-Type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>Hello!</body></html>"
				self.wfile.wrtie(output)
				print output
				return

		except IOError:
			self.send_error(404, "File Not Found %s" %self.path)


def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()

	except KeyboardInterrupt:
		print "^c entered, stopped web server ..."
		server.socket.close()


if __name__ = '__main__':
	main()
