import socket
import os
import mimetypes
from datetime import datetime

HOST = '127.0.0.1'  # Server IP address (localhost)
PORT = 8080         # Server port number
WWW_ROOT = 'www'    # Directory where web files are stored

def log_request(method, path, code):
    # Log the HTTP request details with timestamp, method, path, and status code
    print(f"[{datetime.now()}] {method} {path} -> {code}")

def handle_request(conn):
    # Receive the HTTP request from the client connection
    request = conn.recv(1024).decode('utf-8')
    if not request:
        return  # If request is empty, do nothing

    lines = request.split('\r\n')  # Split request into lines
    request_line = lines[0]         # First line contains the method, path, and HTTP version
    method, path, _ = request_line.split()  # Extract method and path

    # Only allow GET requests, respond 405 for other methods
    if method != 'GET':
        conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
        log_request(method, path, 405)
        return

    # Default to serving index.html if root path is requested
    if path == '/':
        path = '/index.html'

    # Build the full filesystem path to the requested file
    file_path = os.path.join(WWW_ROOT, path.lstrip('/'))
    if os.path.isfile(file_path):
        # Read the file content if it exists
        with open(file_path, 'rb') as f:
            content = f.read()
        # Determine MIME type for the file (default to binary if unknown)
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or 'application/octet-stream'

        # Build HTTP 200 OK response headers + file content
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + content

        # Send the full HTTP response to the client
        conn.sendall(response)
        log_request(method, path, 200)
    else:
        # If file not found, send 404 Not Found response with simple HTML message
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n\r\n"
            "<h1>404 Not Found</h1>"
        ).encode('utf-8')
        conn.sendall(response)
        log_request(method, path, 404)

def start_server():
    # Create a TCP socket and bind it to the specified host and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)  # Start listening for connections, max backlog 5
        print(f"Server avviato su http://{HOST}:{PORT}")
        while True:
            # Accept a client connection
            conn, addr = s.accept()
            with conn:
                # Handle the client request
                handle_request(conn)

if __name__ == '__main__':
    # Run the server when the script is executed
    start_server()
