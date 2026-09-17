import socket
import threading

HOST = "192.168.31.177"
PORT = 23513

clients = []


def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message.encode("utf-8"))
            except:
                pass


def handle_client(client, address):
    print(f"[+] Підключився: {address}")

    while True:
        try:
            data = client.recv(1024)

            if not data:
                break

            message = data.decode("utf-8")
            print(f"{address}: {message}")

            broadcast(f"{address}: {message}", client)

        except ConnectionResetError:
            break

    if client in clients:
        clients.remove(client)

    client.close()
    print(f"[-] Відключився: {address}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print(f"Сервер запущено на порту {PORT}")

while True:
    client, address = server.accept()

    clients.append(client)

    thread = threading.Thread(
        target=handle_client,
        args=(client, address),
        daemon=True
    )
    thread.start()
