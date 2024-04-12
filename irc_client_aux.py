import socket
import threading


def send_message(message):
    print(f'enviando mensaje en el canal {channel}')
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))


def listen_for_messages():
    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print('data'+data)
            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
            # Buscar mensajes de expulsión
            if 'KICK' in data:
                # Dividir el mensaje por espacios para obtener los componentes
                message_parts = data.split()
                # El nombre del usuario expulsado estará en la posición 3 (índice 2)
                kicked_user = message_parts[3]
                # Extraer el canal del mensaje
                channel_name = message_parts[2]
                # Extraer la razón de la expulsión (si existe)
                reason = ' '.join(message_parts[4:]) if len(message_parts) > 3 else "Razón no especificada"
                # Verificar que este usuario es el que fue expulsado para mandarle el sms
                print('usuarioeliminado_'+kicked_user+'_')
                if nickname == kicked_user:
                    print(f"Usuario {kicked_user} ha sido expulsado del canal {channel_name}. Razón: {reason}")
                    join_channel('#miCanal')
        except OSError as e:
            print("Error:", e)
            break

print('Diga canal a unirse')
canal = input()

server = 'irc.dal.net'
port = 6667
channel = "#" + canal
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
