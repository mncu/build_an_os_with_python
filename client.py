
import socket
'''
简单客户端
'''

def client():
    s = socket.socket()
    s.connect(('127.0.0.1',8888))
    try:
        while True:
            input_data = input('please input message').encode()
            s.sendall(input_data)
            print(s.recv(200).decode())
    except:
        s.close()

client()


