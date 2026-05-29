import socket 
from fetch_subnet import fetch_local_ip, fetch_subnet
from scan_subnet import ping_host

def is_port_open(ip, port):
    """
    Check if a TCP port is open on a given IP address.

    Args:
        ip (str): Target IP address.
        port (int): Target port number.

    Returns:
        bool: True if port is open, False otherwise.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        return sock.connect_ex((ip, port)) == 0
    except:
        return False
    finally:
        sock.close()