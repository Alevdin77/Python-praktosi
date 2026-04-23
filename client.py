import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print('[!] Соединение с сервером разорвано')
                break
            print(data.decode('utf-8'))
        except:
            break

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 5001))

thread = threading.Thread(target=receive_messages, args=(client_sock,), daemon=True)
thread.start()

print('Подключено к чату. Введите сообщение, /exit - выход')
while True:
    msg = input()
    if msg == '/exit':
        break
    try:
        client_sock.send(msg.encode('utf-8'))
    except:
        print('Ошибка отправки')
        break

client_sock.close()
print('Вы вышли из чата')