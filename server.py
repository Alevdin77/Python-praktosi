import socket
import threading

clients = []
lock = threading.Lock()

def broadcast(message_bytes, sender=None):
    with lock:
        for c in clients:
            if c != sender:
                try:
                    c.send(message_bytes)
                except:
                    pass

def handle_client(client_sock, addr):
    print('[+] Клиент', addr, 'подключился')
    try:
        client_sock.send('[Система] Добро пожаловать в чат!'.encode('utf-8'))
    except:
        pass
    broadcast(('[Система] ' + str(addr) + ' присоединился к чату').encode('utf-8'), sender=client_sock)

    while True:
        try:
            data = client_sock.recv(1024)
            if not data:
                break
            print('[' + str(addr) + ']', data.decode('utf-8'))
            broadcast(data, sender=client_sock)
        except:
            break

    with lock:
        if client_sock in clients:
            clients.remove(client_sock)
    client_sock.close()
    print('[-] Клиент', addr, 'отключился')
    broadcast(('[Система] ' + str(addr) + ' покинул чат').encode('utf-8'))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('127.0.0.1', 5001))
server_socket.listen()

print('Сервер запущен и ждёт клиентов...')

while True:
    client_sock, addr = server_socket.accept()
    with lock:
        clients.append(client_sock)
    threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True).start()