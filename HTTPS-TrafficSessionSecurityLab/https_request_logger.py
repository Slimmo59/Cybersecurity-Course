# Necessary library imports
from http.server import BaseHTTPRequestHandler, HTTPServer  # To create the HTTP server
from http.cookies import SimpleCookie  # To handle cookies
from urllib.parse import urlparse  # To parse the URL and its parameters
import ssl  # For SSL/TLS (HTTPS) management

# Definition of the class that will handle HTTP requests
class RequestHandler(BaseHTTPRequestHandler):
    # Method that handles GET requests
    def do_GET(self):
        # Extract parameters from the URL (everything following the '?')
        # Example: if the URL is "https://server/path?cookie=123", query will contain "cookie=123"
        parameters = urlparse(self.path).query
        print(f"Received parameters: {parameters}")  # Print the received parameters to the console

        # Send an HTTP response to the client
        self.send_response(200)  # 200 = OK, request successful
        self.send_header('Content-type', 'text/html')  # Specify the content type as HTML
        self.end_headers()  # Finalize the headers section
        
        # Write the response body (sent as bytes)
        self.wfile.write(b"Request received")  
        
# Check if the script is being executed directly (not imported as a module)
if __name__ == '__main__':
    try:
        # Server address configuration
        # '0.0.0.0' listens on all available network interfaces
        # 443 is the standard port for HTTPS traffic
        server_address = ('0.0.0.0', 443)  
             
        # Create an instance of the HTTP server
        httpd = HTTPServer(server_address, RequestHandler)
        
        # SSL/TLS Protocol Configuration
        # Create a new SSL context specifically for server-side TLS
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)  
        
        # Load the SSL certificate and private key
        # Note: 'server.crt' and 'server.key' must exist in the same directory
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')
        
        # Wrap the standard HTTP socket with SSL to enable encryption
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
            
        print('Starting HTTPS Server on port 443...')
        
        # Start the server and keep it running in an infinite loop
        httpd.serve_forever()
        
    # Error handling (e.g., port already in use or missing certificate files)
    except Exception as e:
        print(f"Error: {e}")
