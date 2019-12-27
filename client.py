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
    message = combinaton(message, key)
    return message

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.connect((HOST, PORT))

p = randint(0,10000)
g = randint(0,10000)
a = randint(0,10000)

A = g ** a % p
sock.send(pickle.dumps((p, g, A)))

B = pickle.loads(sock.recv(1024))
key = B ** a % p
message = input("Сообщение: ")
while message != 'exit':
    send_message(sock, message, key)
    print(receive(sock, key))
    message = input()

sock.close()
