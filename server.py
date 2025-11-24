import socket
import threading

HOST = "0.0.0.0"   # listen on all interfaces
PORT = 12345

def handle_client(conn: socket.socket, addr):
    print(f"[+] accepted from {addr}")
    try:
        # session loop: read -> write -> repeat
        while True:
            data = conn.recv(1024)             # recv()
            if not data:                       # EOF (client closed)
                print(f"[!] client {addr} closed")
                break
            msg = data.decode("utf-8", errors="replace")
            print(f"[{addr}] {msg}")
            # echo back (you can change to any protocol/logic)
            conn.send(f"echo: {msg}".encode("utf-8"))   # send()
    except ConnectionResetError:
        print(f"[!] connection reset by {addr}")
    finally:
        conn.close()                            # close()
        print(f"[-] closed {addr}")

def main():
    # socket() -> TCP/IPv4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # setsockopt(): allow fast rebinding during dev
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # bind(): address + port
    server.bind((HOST, PORT))

    # listen(): become a passive socket
    server.listen(8)
    print(f"[server] listening on {HOST}:{PORT}")

    # accept() loop
    while True:
        conn, addr = server.accept()            # accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
