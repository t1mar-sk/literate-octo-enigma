import socket
import threading

HOST = "192.168.31.177"
PORT = 23513


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)

            if not data:
                print("Сервер закрив з'єднання.")
                break

            print("\n" + data.decode("utf-8"))
            print("> ", end="", flush=True)

        except:
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Підключено до чату.")
print("Напиши повідомлення або Ctrl+C для виходу.")

thread = threading.Thread(
    target=receive_messages,
    args=(client,),
    daemon=True
)
thread.start()

while True:
    try:
        message = input("> ")

        if message:
            client.sendall(message.encode("utf-8"))

    except (KeyboardInterrupt, EOFError):
        print("\nВихід...")
        break

client.close()
