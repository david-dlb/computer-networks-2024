import socket
import threading

def send_message(message):
    irc.send(bytes(message, 'UTF-8'))

def listen_for_messages():
    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print(data)
            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
        except OSError as e:
            print("Error:", e)
            break

server = 'irc.dal.net'
port = 6667
channel = '#miCanal'
nickname = 'miUsuario2'
realname = 'Mi Nombre Real2'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

# Iniciar un hilo para escuchar los mensajes del servidor
thread = threading.Thread(target=listen_for_messages)
thread.start()

# Leer mensajes desde la consola y enviar al servidor
while True:
    message = input()
    send_message(message)

irc.close()
