import socket
import time
addr=('127.0.0.1',9999)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(addr)
print "conectei #################################"
time.sleep(10)
