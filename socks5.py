import socket

def handle_socks5(client_socket):
    # 读取客户端请求的认证方法
    client_socket.recv(2)  # 跳过版本号和方法数
    methods = client_socket.recv(1)

    # 直接选择无认证
    client_socket.send(b'\x05\x00')  # 选择无认证的方法

    # 读取客户端请求的命令（连接请求）
    request = client_socket.recv(4)
    if request[1] == 0x01:  # 0x01 是代表连接命令
        # 处理 CONNECT 请求，获取目标地址与端口
        target_address = client_socket.recv(4)
        target_port = client_socket.recv(2)
        target_ip = ".".join(map(str, target_address))
        target_port = int.from_bytes(target_port, "big")

        print(f"Connecting to {target_ip}:{target_port}")

        # 创建一个新的 socket 来连接目标地址
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((target_ip, target_port))

        # 告知客户端连接已成功建立
        client_socket.send(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')

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