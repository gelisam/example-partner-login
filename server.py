#!/usr/local/bin/python3
import http.server
import socketserver

PORT = 8000
SIFT = b"https://siftnlp.keatext.com"
#SIFT = b"http://localhost:3000"

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == "/generate-temp-sift-url":
      token = b"mytoken"
      url = SIFT + b"/partners/ExamplePartner/login?token=" + token
      
      self.send_response(200)
      self.end_headers()
      self.wfile.write(b'{"url": "%s"}' % url)
    else:
      self.send_error(404)


httpd = socketserver.TCPServer(("", PORT), MyRequestHandler)

print("listening to http://localhost:%d" % PORT)
httpd.serve_forever()
