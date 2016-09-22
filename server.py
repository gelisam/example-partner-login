#!/usr/local/bin/python3
import base64
import http.server
import json
import socketserver
import urllib.request

PORT = 8001
KEATEXT = "https://app.keatext.ai"
#KEATEXT = "http://localhost:3000"

# the credentials of the special "partner" user we have created for you when you
# became a Keatext partner
PARTNER_USERNAME = "maelle.blanchette@keatext.com"
PARTNER_PASSWORD = "mypassword"

# the id obtained when you associated an organization with the above user using
# POST https://app.keatext.ai/partner/organizations
ORGANIZATION_ID = "5783d90b927e871d007e339f"


def request_jwt():
  url = "%s/login" % KEATEXT
  json_payload = {"username": PARTNER_USERNAME, "password": PARTNER_PASSWORD}
  binary_payload = json.dumps(json_payload).encode("utf8")
  request = urllib.request.Request(url, binary_payload)
  request.add_header("Content-Type", "application/json")
  request.add_header("Accept", "application/json")
  
  with urllib.request.urlopen(request) as rfile:
    # json_response = {"jwt": {"token": token}}
    binary_response = rfile.read()
    json_response = json.loads(binary_response.decode("utf8"))
    return json_response['jwt']['token']

def request_url(organization_id):
  url = "%s/partner/organizations/%s/login_token" % (KEATEXT, organization_id)
  json_payload = {}
  binary_payload = json.dumps(json_payload).encode("utf8")
  request = urllib.request.Request(url, binary_payload)
  
  jwt = request_jwt()
  auth_header = "Bearer %s" % jwt
  request.add_header("Authorization", auth_header)
  request.add_header("Content-Type", "application/json")
  request.add_header("Accept", "application/json")
  
  with urllib.request.urlopen(request) as rfile:
    # json_response = {"token": token}
    binary_response = rfile.read()
    json_response = json.loads(binary_response.decode("utf8"))
    return json_response['url']

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
  def do_POST(self):
    if self.path == "/generate-temp-keatext-url":
      # ExamplePartner is associated with a single organization, "Lucille", so we
      # hardcode her organization id above instead of bothering to maintain an
      # HTTP session.
      url = request_url(ORGANIZATION_ID)
      print("url", url)
      
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
