
import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 54321))
clientsocket.send(bytes("Hallo michiel", 'UTF-8'))