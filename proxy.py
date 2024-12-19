import socket
import threading
import sys
from socks5 import handle_socks5
from socks4 import handle_socks4

def start_proxy_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Proxy server listening on {host}:{port}")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Connection from {client_addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    try:
        # 读取 SOCKS 版本号（第一个字节）
        version = client_socket.recv(1)
        if not version:
            return

        # 判断 SOCKS 版本
        if version == b'\x05':  # SOCKS5
            handle_socks5(client_socket)
        elif version == b'\x04':  # SOCKS4
            handle_socks4(client_socket)
        else:
            print("Unsupported SOCKS version.")
            client_socket.close()
    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()

if __name__ == "__main__":
    host = "0.0.0.0"  # 绑定到所有接口
    port = 1080        # 监听端口
    start_proxy_server(host, port)