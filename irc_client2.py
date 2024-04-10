import socket
import threading

def send_message(message):
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))

def quit_irc():
    irc.send(bytes('QUIT\r\n', 'UTF-8'))
    irc.close()
    print("Desconectado del servidor IRC.")

def userhost_query(nicknames):
    nicknames_str = ' '.join(nicknames)
    irc.send(bytes('USERHOST ' + nicknames_str + '\r\n', 'UTF-8'))

def invite_user(nickname, channel):
    irc.send(bytes('INVITE ' + nickname + ' ' + channel + '\r\n', 'UTF-8'))

def set_topic(new_topic):
    irc.send(bytes('TOPIC ' + channel + ' :' + new_topic + '\r\n', 'UTF-8'))

def wallops_message(message):
    irc.send(bytes('WALLOPS :' + message + '\r\n', 'UTF-8'))
def send_action():
    action = input("action: ")
    irc.send(bytes('PRIVMSG ' + channel + ' :\x01ACTION ' + action + '\x01\r\n', 'UTF-8'))

def listen_for_messages():
    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print(data)
            if data.startswith('302'):
                print("Userhost information:", data.split()[2:])
            if data.startswith('353'):
                print("Usuarios en el canal: ", data.split()[3:])
            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
            if data.startswith('ERROR'):
                handle_error(data)
        except OSError as e:
            print("Error al escuchar mensajes:", e)
            break

def whois_user(nickname):
    irc.send(bytes('WHOIS ' + nickname + '\\r\\n', 'UTF-8'))

def whowas_user(nickname):
    irc.send(bytes('WHOWAS ' + nickname + '\\r\\n', 'UTF-8'))

def who_channel(channel):
    irc.send(bytes('WHO ' + channel + '\\r\\n', 'UTF-8'))

def change_user():
    new_nickname = input("Ingrese el nuevo nombre de usuario: ")
    global nickname 
    nickname = new_nickname
    irc.send(bytes('NICK ' + new_nickname + '\r\n', 'UTF-8'))

def stats():
    irc.send(bytes('STATS' + '\r\n', 'UTF-8'))

def part_channel():
    global channel # Asegúrate de que puedas modificar la variable global
    if channel: # Verifica que el canal no esté vacío
        irc.send(bytes('PART ' + channel + '\r\n', 'UTF-8'))
    else:
        print("No hay un canal al que unirse.")

def list_names():
    irc.send(bytes('NAMES ' + channel + '\r\n', 'UTF-8'))

def list_users(channel_name):
    irc.send(bytes('NAMES ' + channel_name + '\r\n', 'UTF-8'))

def join_channel(channel_name):
    # Asegúrate de que el nombre del canal no esté vacío
    if channel_name:
        irc.send(bytes('JOIN ' + channel_name + '\r\n', 'UTF-8'))
        channel = channel_name
    else:
        print("El nombre del canal no puede estar vacío.")

def create_channel(channel_name):
    # Asegúrate de que el nombre del canal no esté vacío
    if channel_name:
        irc.send(bytes('CREATE ' + channel_name + '\r\n', 'UTF-8'))
    else:
        print("El nombre del canal no puede estar vacío.")

def kick_user(nickname):
    irc.send(bytes('KICK ' + channel + ' ' + nickname + ' :You are kicked!\\r\\n', 'UTF-8'))

def handle_error(error_message):
    print("Error recibido del servidor:", error_message)

print('Diga canal a unirse')
canal = input()

server = 'irc.dal.net'
port = 6667
channel = "#" + canal
nickname = 'miUsuario'
realname = 'Mi Nombre Real'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

# Iniciar un hilo para escuchar los mensajes del servidor
thread = threading.Thread(target=listen_for_messages)
thread.start()

while True:
    message = input()
    if message.startswith("/userhost "):
        nicknames = message[10:].split()
        userhost_query(nicknames)
        continue
    if message.startswith("/wallops "):
        wallops_message(message[9:])
        continue
    if message.startswith("/whois "):
        whois_user(message[7:])
        continue
    if message.startswith("/whowas "):
        whowas_user(message[8:])
        continue
    if message.startswith("/who "):
        who_channel(message[5:])
        continue
    if message.startswith("/nick "):
        change_user()
        continue
    if message.startswith("/stats"):
        stats()
        continue
    if message.startswith("/part"):
        part_channel()
        continue
    if message.startswith("/names"):
        list_names()
        continue
    if message.startswith("/users"):
        list_users(channel)
        continue
    if message.startswith("/action "):
        send_action(message[8:])
        continue
    if message.startswith("/topic "):
        set_topic(message[7:])
        continue
    if message.startswith("/joinChanel"):
        chanel = message.split(" ")[1]
        join_channel(chanel)
        continue
    if message.startswith("/createChanel"):
        print('creando un canal')
        chanel = message.split(" ")[1]
        create_channel(chanel)
        continue
    if message.startswith("/kick"): # para eliminar a un usuario del canal
        usertoKick = message.split(" ")[1]
        kick_user(usertoKick)
        continue
    if message.startswith("/invite "):
        # Asume que el comando tiene el formato "/invite nickname #channel"
        parts = message[8:].split(' ')
        if len(parts) == 2:
            invite_user(parts[0], parts[1])
        else:
            print("Uso incorrecto del comando /invite. Debe ser /invite nickname #channel")
        continue
    if message.startswith("/quit"):
        quit_irc()
        break
    send_message(message)

irc.close()
