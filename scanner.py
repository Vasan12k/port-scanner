import socket
import threading


def scan_port(target_ip: str, port: int, timeout: float = 0.5) -> bool:
    """Return True if port is open on target_ip."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((target_ip, port)) == 0
    except Exception:
        return False


def resolve_target(target: str) -> str:
    """Resolve a hostname to an IP address."""
    return socket.gethostbyname(target)


def scan_target(target: str, start_port: int = 1, end_port: int = 100, timeout: float = 0.5) -> list[int]:
    """Scan ports in [start_port, end_port] on the target and return open ports."""
    target_ip = resolve_target(target)
    open_ports: list[int] = []
    threads = []
    lock = threading.Lock()

    def worker(port: int):
        if scan_port(target_ip, port, timeout):
            with lock:
                open_ports.append(port)

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=worker, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    open_ports.sort()
    return open_ports


if __name__ == "__main__":
    target = input("Enter target IP or domain: ")

    try:
        target_ip = resolve_target(target)
    except socket.gaierror:
        print("Invalid target!")
        exit(1)

    print(f"\nScanning {target_ip}...\n")

    try:
        open_ports = scan_target(target)
    except Exception as e:
        print(f"Scan failed: {e}")
        exit(1)

    if open_ports:
        for p in open_ports:
            print(f"[OPEN] Port {p}")
    else:
        print("No open ports found in the range.")

    print("\nScan completed.")