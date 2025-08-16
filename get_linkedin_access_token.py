"""
Get a LinkedIn OAuth access token and save it to .env as LI_ACCESS_TOKEN.
Opens the LinkedIn login page, captures the authorization code, exchanges it for an access token, and stores it locally.
"""

import os
import webbrowser
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode

PORT = 8000
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
REDIRECT_URI = f"http://localhost:{PORT}/callback"

auth_code = [None]

class CallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def do_GET(self):
        if self.path.startswith('/callback'):
            query = urlparse(self.path).query
            params = parse_qs(query)
            if 'code' in params:
                auth_code[0] = params['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h1>Authentication complete. You can close this window.</h1>")
                threading.Thread(target=server.shutdown, daemon=True).start()

server = HTTPServer(('localhost', PORT), CallbackHandler)
threading.Thread(target=server.serve_forever, daemon=True).start()

auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urlencode({
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "profile",
    "state": "tutorial_state"
})
webbrowser.open(auth_url)

server.serve_forever()

token_url = "https://www.linkedin.com/oauth/v2/accessToken"
token_data = {
    "grant_type": "authorization_code",
    "code": auth_code[0],
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET
}

response = requests.post(token_url, data=token_data)
access_token = response.json().get("access_token")

if access_token:
    with open(".env", "a") as f:
        f.write(f"LI_ACCESS_TOKEN={access_token}\n")