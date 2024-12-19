import socket

def handle_socks4(client_socket):
    # 读取客户端请求
    request = client_socket.recv(9)  # 读取请求头
    command = request[1]

    if command == 0x01:  # 0x01 是代表连接命令
        target_port = request[2:4]
        target_ip = request[4:8]

        target_ip = ".".join(map(str, target_ip))
        target_port = int.from_bytes(target_port, "big")

        print(f"Connecting to {target_ip}:{target_port}")

        # 创建新的 socket 连接目标服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((target_ip, target_port))

        # 响应客户端连接成功
        client_socket.send(b'\x00\x5a\x00\x00\x00\x00\x00\x00')  # 连接成功的响应

        # 转发数据
        forward_data(client_socket, server_socket)
    else:
        client_socket.close()

def forward_data(client_socket, server_socket):
    while True:
        # 从客户端读取数据并转发到目标服务器
        data = client_socket.recv(4096)
        if not data:
            break
        server_socket.send(data)

        # 从目标服务器读取数据并转发到客户端
        data = server_socket.recv(4096)
        if not data:
            break
        client_socket.send(data)

    client_socket.close()
    server_socket.close()