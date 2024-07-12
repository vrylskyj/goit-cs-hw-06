# main.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
from datetime import datetime
import pymongo

# Налаштування бази даних MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client['mydatabase']
collection = db['messages']

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/message':
            self.path = '/message.html'
        elif self.path == '/error':
            self.path = '/error.html'
        elif not self.path.startswith('/static/'):
            self.send_error(404, 'File Not Found: %s' % self.path)
            self.path = '/error.html'

        try:
            if self.path.startswith('/static/'):
                # Обробка статичних ресурсів
                file_path = '.' + self.path
                with open(file_path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/css' if self.path.endswith('.css') else 'image/png')
                self.end_headers()
                self.wfile.write(content)
            else:
                # Обробка HTML файлів
                file_path = '.' + self.path
                with open(file_path, 'r') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            self.path = '/error.html'
            with open('.' + self.path, 'r') as file:
                content = file.read()
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())

    def do_POST(self):
        if self.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            data = dict(item.split('=') for item in post_data.split('&'))
            data['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

            # Відправка даних на Socket-сервер
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('socket_server', 5000))
                s.sendall(json.dumps(data).encode())

            self.send_response(302)
            self.send_header('Location', '/message')
            self.end_headers()

def run_http_server():
    with HTTPServer(("", 3000), RequestHandler) as httpd:
        print("HTTP server running on port 3000")
        httpd.serve_forever()

if __name__ == "__main__":
    run_http_server()
