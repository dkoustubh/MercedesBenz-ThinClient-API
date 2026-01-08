import http.server
import socketserver
import urllib.request
import urllib.error
import json
import sys

# Configuration
PORT = 8081 # Using 8081 to avoid conflict with your running server
REMOTE_BASE_URL = "http://192.168.10.152:8080/api/production/get_andon_info"

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if the request is for our proxy API
        if self.path.startswith('/api/andon/'):
            # Extract line_id from the path (e.g. /api/andon/1 -> 1)
            try:
                line_id = self.path.split('/')[-1]
                target_url = f"{REMOTE_BASE_URL}/{line_id}"
                
                print(f"Proxying request: {self.path} -> {target_url}")
                
                # Make the request to the Windows machine
                with urllib.request.urlopen(target_url) as response:
                    data = response.read()
                    status = response.status
                    
                # Send the response back to the browser
                self.send_response(status)
                self.send_header('Content-type', 'application/json')
                # Important: Allow access from anywhere (CORS)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
                
            except urllib.error.URLError as e:
                # Handle connection errors (e.g. Windows machine offline)
                self.send_response(502)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_msg = json.dumps({"success": False, "message": f"Proxy Error: {str(e.reason)}"}).encode()
                self.wfile.write(error_msg)
                
            except Exception as e:
                # Handle other errors
                self.send_response(500)
                self.end_headers()
                print(f"Error: {e}")
                
        else:
            # For all other requests, serve files (HTML, CSS, etc.)
            super().do_GET()

# Allow address reuse to prevent "Address already in use" errors on restart
socketserver.TCPServer.allow_reuse_address = True

print(f"Starting Proxy Server on http://localhost:{PORT}")
print(f"Dashboard: http://localhost:{PORT}/ThinClientTestv2.html")
print("Press Ctrl+C to stop")

with socketserver.TCPServer(("", PORT), ProxyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()
