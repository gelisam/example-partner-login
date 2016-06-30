#!/usr/local/bin/python3
import http.server
import json
import socketserver

PORT = 8000
SIFT = "https://siftnlp.keatext.com"
#SIFT = "http://localhost:3000"

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == "/generate-temp-sift-url":
      token = "mytoken"
      url = SIFT + "/partners/ExamplePartner/login?token=" + token
      json_response = {"url": url}
      binary_response = bytes(json.dumps(json_response), "utf8")
      
      self.send_response(200)
      self.end_headers()
      self.wfile.write(binary_response)
    else:
      self.send_error(404)


httpd = socketserver.TCPServer(("", PORT), MyRequestHandler)

print("listening to http://localhost:%d" % PORT)
httpd.serve_forever()
