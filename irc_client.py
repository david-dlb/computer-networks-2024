import socket
import threading

def send_message(message):
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))


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

print('Diga canal a unirse')
canal = input()

server = 'irc.dal.net'
port = 6667
channel = canal
nickname = 'miUsuario3'
realname = 'MiNombreReal3'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

# Iniciar un hilo para escuchar los mensajes del servidor
thread = threading.Thread(target=listen_for_messages)
thread.start()

def whois_user(nickname):
    irc.send(bytes('WHOIS ' + nickname + '\r\n', 'UTF-8'))

def whowas_user(nickname):
    irc.send(bytes('WHOWAS ' + nickname + '\r\n', 'UTF-8'))

def who_channel(channel):
    irc.send(bytes('WHO ' + channel + '\r\n', 'UTF-8'))

while True:
    message = input()
    if message.startswith("/whois "):
        whois_user(message[7:])
        continue
    if message.startswith("/whowas "):
        whowas_user(message[8:])
        continue
    if message.startswith("/who "):
        print("ho")
        who_channel(message[5:])
        continue
    if message.startswith("/quit"):
        break
    send_message(message)

irc.close()
