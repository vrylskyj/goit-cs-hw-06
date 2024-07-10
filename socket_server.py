import socket
import json
import pymongo

# Налаштування бази даних MongoDB
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client['mydatabase']
collection = db['messages']

def start_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 5000))
        s.listen()
        print("Socket server running on port 5000")

        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                if data:
                    message = json.loads(data.decode())
                    collection.insert_one(message)
                    print(f"Message saved: {message}")

if __name__ == "__main__":
    start_socket_server()
