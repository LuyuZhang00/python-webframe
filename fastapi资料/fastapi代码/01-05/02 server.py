# web应用程序：遵循http协议
import socket

sock = socket.socket()

sock.bind(("127.0.0.1", 8090))
sock.listen(5)
while 1:
    conn, addr = sock.accept()  # 阻塞等待客户端连接
    data = conn.recv(1024)
    print("客户端发送的请求信息:\n",data)
    conn.send(b'HTTP/1.1 200 ok\r\nserver:yuan\r\ncontent-type:application/json\r\n\r\n{"user_id":101}')
    conn.close()


