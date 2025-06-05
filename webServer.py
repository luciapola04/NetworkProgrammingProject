import socket
import os
import mimetypes
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8080
WWW_ROOT = 'www'

def log_request(method, path, code):
    print(f"[{datetime.now()}] {method} {path} -> {code}")

def handle_request(conn):
    request = conn.recv(1024).decode('utf-8')
    if not request:
        return

    lines = request.split('\r\n')
    request_line = lines[0]
    method, path, _ = request_line.split()

    if method != 'GET':
        conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
        log_request(method, path, 405)
        return

    if path == '/':
        path = '/index.html'

    file_path = os.path.join(WWW_ROOT, path.lstrip('/'))
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or 'application/octet-stream'
        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime_type}\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode('utf-8') + content
        conn.sendall(response)
        log_request(method, path, 200)
    else:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n\r\n"
            "<h1>404 Not Found</h1>"
        ).encode('utf-8')
        conn.sendall(response)
        log_request(method, path, 404)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Server avviato su http://{HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                handle_request(conn)

if __name__ == '__main__':
    start_server()
