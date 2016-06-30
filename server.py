#!/usr/local/bin/python3
import http.server
import socketserver

PORT = 8000

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == "/generate-temp-sift-token":
      token = b"mytoken"
      
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b'{"token": "%s"}' % token)
    else:
      self.send_error(404)


httpd = socketserver.TCPServer(("", PORT), MyRequestHandler)

print("listening to http://localhost:%d" % PORT)
httpd.serve_forever()
