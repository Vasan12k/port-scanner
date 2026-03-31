import socket

# Ask user for target
target = input("Enter target IP or domain: ")

# Convert domain to IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid target!")
    exit()

print(f"\nScanning target: {target_ip}\n")

# Scan ports
for port in range(1, 101):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)

    result = s.connect_ex((target_ip, port))

    if result == 0:
        print(f"[OPEN] Port {port}")

    s.close()

print("\nScan completed.")