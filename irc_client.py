import socket
import threading

server = 'irc.dal.net'
port = 6667
channel = '#testChannel2'
nickname = 'miUsuario2'
realname = 'MiNombreReal2'

def send_message(message):
    print(f'enviando mensaje en el canal {channel}')
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))


def listen_for_messages():
    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print(data)
            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
            # Buscar mensajes de expulsión
            if 'KICK' in data and nickname in data:
                # print(f"Has sido expulsado del canal {channel}. Razón: {data.split(':', 1)[1]}")
                print('---------------------------------')
                print(f"Has sido expulsado del canal {channel}. Por alguna razon")
                print('---------------------------------')
                join_channel('#miCanal')
        except OSError as e:
            print("Error:", e)
            break

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

def join_channel(channel_name):
    global channel
    # Asegúrate de que el nombre del canal no esté vacío
    if channel_name:
        irc.send(bytes('JOIN ' + channel_name + '\r\n', 'UTF-8'))
        channel = channel_name
    else:
        print("El nombre del canal no puede estar vacío.")

def who_channel(channel):
    irc.send(bytes('WHO ' + channel + '\r\n', 'UTF-8'))

while True:
    print(f'Estas en el canal {channel}')
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
    if message.startswith("/joinChanel"):
        chanel = message.split(" ")[1]
        join_channel(chanel)
        continue
    if message.startswith("/quit"):
        break
    send_message(message)

irc.close()
