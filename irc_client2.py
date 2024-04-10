import socket
import threading


# -----------------------------------------------------------
# Credencial y configuracion de cliente
# ------------------------------------------------------------

# print('Diga su nombre de usuario')
# nickname = input()

# print('Diga su nombre real')
# realname = input()

# print('Diga canal a unirse')
# channel = input()

server = 'irc.dal.net'
port = 6667
channel = "#miCanal"
nickname = 'miUsuario1'
realname = 'Mi Nombre Real1'


# --------------------------------------------------
# Funcionalidades del cliente
# ----------------------------------------------------

# Enviar el mensaje
def send_message(message):
    print(f'enviando mensaje en el canal {channel}')
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))

# Salir del cliente
def quit_irc():
    irc.send(bytes('QUIT\r\n', 'UTF-8'))
    irc.close()
    print("Desconectado del servidor IRC.")

# 
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
            print('----------------------------')
            print('data : '+data)
            print('----------------------------')

            if data.startswith('302'):
                print("Userhost information:", data.split()[2:])
            if data.startswith('353'):
                print("Usuarios en el canal: ", data.split()[3:])
            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))
            if data.startswith('ERROR'):
                handle_error(data)
            # Buscar mensajes de expulsión
            if 'KICK' in data and nickname in data:
                # Dividir el mensaje por espacios para obtener los componentes
                message_parts = data.split()
                # El nombre del usuario expulsado estará en la posición 3 (índice 2)
                kicked_user = message_parts[3]
                # Extraer el canal del mensaje
                channel_name = message_parts[2]
                # Extraer la razón de la expulsión (si existe)
                reason = ' '.join(message_parts[4:]) if len(message_parts) > 3 else "Razón no especificada"
                print('usuarioeliminado_'+kicked_user+'_')
                if nickname == kicked_user:
                    print(f"Usuario {kicked_user} ha sido expulsado del canal {channel_name}. Razón: {reason}")
                    join_channel('#miCanal')
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
    global channel
    # Asegúrate de que el nombre del canal no esté vacío
    if channel_name:
        irc.send(bytes('JOIN ' + channel_name + '\r\n', 'UTF-8'))
        channel = channel_name
    else:
        print("El nombre del canal no puede estar vacío.")

def part_channel():
    global channel
    if channel: # Verifica que el canal no esté vacío
        irc.send(bytes('PART ' + channel + '\r\n', 'UTF-8'))
        print(f"Has abandonado el canal {channel}.")
        channel = '' # Limpia el nombre del canal para indicar que no estás en un canal
    else:
        print("No estás en un canal para abandonar.")

# def create_channel(channel_name):
#     # Asegúrate de que el nombre del canal no esté vacío
#     if channel_name:
#         irc.send(bytes('CREATE ' + channel_name + '\r\n', 'UTF-8'))
#     else:
#         print("El nombre del canal no puede estar vacío.")

def kick_user(nickname):
    irc.send(bytes('KICK ' + channel + ' ' + nickname + ' :You are kicked!\\r\\n', 'UTF-8'))

def handle_error(error_message):
    print("Error recibido del servidor:", error_message)



irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

# Iniciar un hilo para escuchar los mensajes del servidor
thread = threading.Thread(target=listen_for_messages)
thread.start()

while True:
    print(f'Estas en el canal {channel}')
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
        part_channel()
        join_channel(chanel)
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
