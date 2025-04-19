import socket
import threading
import random

clients = {}
positions = {}

def handle_client(client, addr):
    name = client.recv(1024).decode()
    clients[name] = client
    positions[name] = 1
    print(f"{name} joined from {addr}")
    broadcast_positions()

    while True:
        try:
            data = client.recv(1024).decode()
            if data == "roll":
                dice = random.randint(1, 6)
                current_pos = positions[name]

                if current_pos + dice <= 100:
                    new_pos = current_pos + dice
                    new_pos = check_snake_ladder(new_pos)
                    positions[name] = new_pos
                    broadcast_positions()

                    if positions[name] == 100:
                        broadcast_message(f"{name} wins the game!")
                        print(f"{name} wins the game!")
                        break
                else:
                    client.send("Invalid move. You need an exact roll to reach 100.".encode())
        except:
            print(f"{name} disconnected")
            del clients[name]
            del positions[name]
            broadcast_positions()
            break

def broadcast_positions():
    for name, client in clients.items():
        try:
            message = "positions:" + str(positions)
            client.send(message.encode())
        except:
            pass
        
def broadcast_message(message):
    """Broadcast a message to all clients."""
    for client in clients.values():
        try:
            client.send(message.encode())
        except:
            pass

def check_snake_ladder(pos):
    snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
    ladders = {2: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
    if pos in snakes:
        return snakes[pos]
    elif pos in ladders:
        return ladders[pos]
    return pos

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.204.139', 12345))  # Replace with your server IP
    server.listen(5)
    print("Server started on port 12345")

    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr)).start()

if __name__ == "__main__":
    start_server()


