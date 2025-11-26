import socket

# change this to the server machine name or IP if you’re not on the same PC
HOSTNAME = "localhost"       # demo: "localhost", or your LAN IP like "192.168.1.20"
PORT = 12345

def main():
    # gethostbyname(): hostname -> IPv4
    ip = socket.gethostbyname(HOSTNAME)
    print(f"[client] resolved {HOSTNAME} -> {ip}")

    # socket() + connect()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, PORT))
    print(f"[client] connected to {ip}:{PORT}")
    print("type a line and press Enter (empty line = quit)")

    try:
        while True:
            line = input("> ")
            if line == "":
                break  # EOF for our little protocol
            s.send(line.encode("utf-8"))     # send()
            reply = s.recv(1024)             # recv()
            if not reply:
                print("[client] server closed")
                break
            print(reply.decode("utf-8", errors="replace"))
    finally:
        s.close()                             # close()
        print("[client] closed")

if __name__ == "__main__":
    main()
