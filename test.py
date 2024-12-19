import socket
import socks
import threading

def handle_client(client_socket):
    # 设置客户端代理为 SOCKS5
    socks.set_default_proxy(socks.SOCKS5, '192.168.3.7', 1080)
    socket.socket = socks.socksocket

    # 读取客户端请求并转发
    request = client_socket.recv(4096)
    print(request)

    # 返回响应（这里只是示例，具体逻辑需要根据应用进行修改）
    client_socket.send(b'HTTP/1.1 200 OK\r\n\r\n')
    client_socket.close()

def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 1080))  # SOCKS5 监听地址和端口
    server.listen(5)

    print("Proxy Server listening on 0.0.0.0:1080")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()