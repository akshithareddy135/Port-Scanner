import socket 
from concurrent.futures import ThreadPoolExecutor, as_completed
from fetch_subnet import fetch_local_ip, fetch_subnet
from scan_subnet import ping_host
from sweep_ports import is_port_open


if __name__ == "__main__":
    # Get local IP and subnet
    local_ip = fetch_local_ip()
    print("Local IP:", local_ip)

    subnet = fetch_subnet(local_ip)
    print("Subnet:", subnet)

    # Find live hosts on the subnet
    print("\n[+] Scanning for live hosts...")
    live_hosts = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {
            executor.submit(ping_host, f"{subnet}{i}"): f"{subnet}{i}"
            for i in range(1, 255)
        }

        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                alive = future.result()
            except Exception:
                alive = False
            if alive:
                print(f"{ip} is alive")
                live_hosts.append(ip)

    print("\nLive Hosts Found:", live_hosts)

    # Scan open ports for each live host
    for ip in live_hosts:
        print(f"\n[+] Scanning ports on {ip}...")
        open_ports = []

        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_port = {
                executor.submit(is_port_open, ip, port): port
                for port in range(1, 101)  # Ports 1-100
            }

            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    open_ = future.result()
                except Exception:
                    open_ = False
                if open_:
                    print(f"Port {port} is open on {ip}")
                    open_ports.append(port)

        # Show scan summary for the host
        if open_ports:
            print(f"[✓] Scan complete for {ip}. Open ports: {sorted(open_ports)}")
        else:
            print(f"[✗] Scan complete for {ip}. No open ports found.")