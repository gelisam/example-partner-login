#!/usr/local/bin/python3
import base64
import http.server
import json
import socketserver
import urllib.request

PORT = 8000
SIFT = "https://siftnlp.keatext.com"
#SIFT = "http://localhost:3000"

PARTNER_USERNAME = b"maelle.blanchette@keatext.com"
PARTNER_PASSWORD = b"mypassword"


def request_token(user_email):
  url = "%s/api/v1/partner/login_token" % SIFT
  json_payload = {"email": user_email}
  binary_payload = json.dumps(json_payload).encode("utf8")
  request = urllib.request.Request(url, binary_payload)
  
  # this base64 rigmarole is the "basic auth" standard.
  auth_string = PARTNER_USERNAME + b":" + PARTNER_PASSWORD
  auth_header = b"Basic " + base64.encodestring(auth_string).rstrip()
  request.add_header("Authorization", auth_header)
  request.add_header("Content-Type", "application/json")
  
  with urllib.request.urlopen(request) as rfile:
    # json_response = {"token": token}
    binary_response = rfile.read()
    json_response = json.loads(binary_response.decode("utf8"))
    return json_response['token']

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == "/generate-temp-sift-url":
      # ExamplePartner only has a single user, "Lucille", so we hardcode her email
      # here instead of bothering to maintain an HTTP session.
      token = request_token("lucille.blanchette@keatext.com")
      
      url = "%s/partner-login?token=%s" % (SIFT, token)
      json_response = {"url": url}
      binary_response = json.dumps(json_response).encode("utf8")
      
      self.send_response(200)
      self.end_headers()
      self.wfile.write(binary_response)
    else:
      self.send_error(404)


httpd = socketserver.TCPServer(("", PORT), MyRequestHandler)

print("listening to http://localhost:%d" % PORT)
httpd.serve_forever()
