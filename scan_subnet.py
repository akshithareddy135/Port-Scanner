from pythonping import ping

def ping_host(host):
    response = ping(host, count=1, timeout=1)
    return response.success()