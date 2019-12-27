import socket
import pickle
from random import randint

def combinaton(P1, key):
    P2 = []
    for i in range(len(P1)):
        P2 += chr(ord(P1[i]) ^ key)
    return ''.join(P2)

def send_message(sock, message, key):
    message = combinaton(message, key)
    sock.send(pickle.dumps(message))

def receive(sock, key):
    message = pickle.loads(sock.recv(1024))
    message = combinaton(message,key)
    return message

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

message = conn.recv(1024)

p, g, A = pickle.loads(message)
b = randint(0, 10000)
B = g ** b % p
conn.send(pickle.dumps(B))
key = A ** b % p


while True:
    try:
        message = receive(conn, key)
        print(message)
        send_message(conn, 'Сообщение успешно получено и расшифровано', key)
    except EOFError: 
        break

conn.close()
