import socket

def test_proxy(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 尝试通过 SOCKS 代理连接到外部服务器
        s.connect((host, port))
        print(f"Successfully connected to {host}:{port} through SOCKS proxy.")
    except Exception as e:
        print(f"Failed to connect to {host}:{port} through SOCKS proxy: {e}")
    finally:
        s.close()

# 通过 SOCKS5 代理测试连接
test_proxy("www.google.com", 80)  # 连接目标服务器