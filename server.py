
from scheduler import Scheduler
import socket
import system_call

'''
实现一个简单的应用协程的 web 服务器。
'''

def handler(conn,addr):
    try:
        while True:
            yield system_call.WaitRead(conn)
            data = conn.recv(200).decode()
            print('the %s sends a message: %s' %(addr, data))
            conn.sendall('hello'.encode())
    except Exception:
        conn.close()
        print('-----%s is closed-----'%addr[0])

def server():
    print('start the simple web server')
    s = socket.socket()
    s.bind(('127.0.0.1',8888))
    s.listen(5)
    while True:
        yield system_call.WaitRead(s)
        conn, addr = s.accept()
        yield system_call.NewTask(handler(conn,addr))



s = Scheduler()
# s.new(alive())
s.new(server())
s.main_loop()