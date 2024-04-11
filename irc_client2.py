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

# print('Ingrese la contraseña para el servidor IRC:')
# password = input()

server = 'irc.dal.net'
port = 6667
channel = "#miCanal2"
nickname = 'miUsuario2'
realname = 'Mi Nombre Real2'
password = 'password2'

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
            data = irc.recv(2048)
            try:
                # Intenta decodificar los datos como UTF-8
                data = data.decode('UTF-8')
            except UnicodeDecodeError:
                # Si falla, intenta decodificar como ISO-8859-1
                data = data.decode('ISO-8859-1')
            print('----------------------------')
            print('----------------------------')
            print('data : '+data)
            print('----------------------------')

            if data.startswith('302'):
                print("Userhost information:", data.split()[2:])
            if data.startswith('353'):
                print("Usuarios en el canal: ", data.split()[3:])
            # Manejar la respuesta al comando LIST
            if data.startswith('321'):
                print("Lista de canales:")
            elif data.startswith('322'):
                print(data.split()[3]) # Imprime el nombre del canal
            elif data.startswith('323'):
                print("Fin de la lista de canales.")

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

def list_channels():
    irc.send(bytes('LIST\r\n', 'UTF-8'))

def list_users(channel_name):
    irc.send(bytes('NAMES ' + channel_name + '\r\n', 'UTF-8'))

def connect_to_server(server_name):
    # Asegúrate de que el nombre del servidor no esté vacío
    if server_name:
        irc.send(bytes(f'SERVER {server_name}\r\n', 'UTF-8'))
    else:
        print("El nombre del servidor no puede estar vacío.")
        
def list_connected_servers():
    irc.send(bytes('LINKS\r\n', 'UTF-8'))

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
    send_message('KICK ' + channel + ' ' + nickname + ' :You are kicked!\\r\\n')

def ban_user(channel, nickname):
    # Asegúrate de que el canal y el nickname no estén vacíos
    if channel and nickname:
        irc.send(bytes(f'MODE {channel} +b {nickname}\r\n', 'UTF-8'))
    else:
        print("El canal y el nickname no pueden estar vacíos.")

def unban_user(channel, nickname):
    # Asegúrate de que el canal y el nickname no estén vacíos
    if channel and nickname:
        irc.send(bytes(f'MODE {channel} -b {nickname}\r\n', 'UTF-8'))
    else:
        print("El canal y el nickname no pueden estar vacíos.")

def set_channel_password(channel, password):
    # Asegúrate de que el canal y la contraseña no estén vacíos
    if channel and password:
        irc.send(bytes(f'MODE {channel} +k {password}\r\n', 'UTF-8'))
    else:
        print("El canal y la contraseña no pueden estar vacíos.")

def make_channel_invite_only(channel):
    # Asegúrate de que el canal no esté vacío
    if channel:
        irc.send(bytes(f'MODE {channel} +i\r\n', 'UTF-8'))
    else:
        print("El nombre del canal no puede estar vacío.")

def remove_channel_invite_only(channel):
    # Asegúrate de que el canal no esté vacío
    if channel:
        irc.send(bytes(f'MODE {channel} -i\r\n', 'UTF-8'))
    else:
        print("El nombre del canal no puede estar vacío.")
def remove_channel_password(channel):
    # Asegúrate de que el canal no esté vacío
    if channel:
        irc.send(bytes(f'MODE {channel} -k\r\n', 'UTF-8'))
    else:
        print("El nombre del canal no puede estar vacío.")
def change_user_permissions(channel, nickname, mode):
    # Asegúrate de que el canal, el nickname y el modo no estén vacíos
    if channel and nickname and mode:
        irc.send(bytes(f'MODE {channel} {mode} {nickname}\r\n', 'UTF-8'))
    else:
        print("El canal, el nickname y el modo no pueden estar vacíos.")

def handle_error(error_message):
    print("Error recibido del servidor:", error_message)



# Crear el socket y conectar al servidor
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

# Enviar credenciales para iniciar sesion
irc.send(bytes('PASS ' + password + '\r\n', 'UTF-8'))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))


# Iniciar un hilo para escuchar los mensajes del servidor
thread = threading.Thread(target=listen_for_messages)
thread.start()

while True:
    print(f'Estas en el canal {channel}')
    message = input()
    if message.startswith("/server"):
        # Asume que el comando tiene el formato "/server server_name"
        server_name = message[8:]
        connect_to_server(server_name)
        continue
    if message.startswith("/links"):
        list_connected_servers()
        continue
    if message.startswith("/removeinviteonly"):
        # Asume que el comando tiene el formato "/removeinviteonly #channel"
        channel_name = message[17:]
        remove_channel_invite_only(channel_name)
        continue
    if message.startswith("/inviteonly"):
        # Asume que el comando tiene el formato "/inviteonly #channel"
        channel_name = message[12:]
        make_channel_invite_only(channel_name)
        continue
    if message.startswith("/password"):
        # Asume que el comando tiene el formato "/password #channel contraseña"
        parts = message[9:].split(' ', 1)
        if len(parts) == 2:
            channel_name, password = parts
            set_channel_password(channel_name, password)
        else:
            print("Uso incorrecto del comando /password. Debe ser /password #channel contraseña")
        continue
    if message.startswith("/op"):
        # Asume que el comando tiene el formato "/op nickname"
        nickname = message[4:]
        change_user_permissions(channel, nickname, '+o')
        continue
    if message.startswith("/deop"):
        # Asume que el comando tiene el formato "/deop nickname"
        nickname = message[6:]
        change_user_permissions(channel, nickname, '-o')
        continue
    if message.startswith("/ban"):
        # Asume que el comando tiene el formato "/ban nickname #channel"
        parts = message[5:].split(' ')
        if len(parts) == 2:
            ban_user(parts[1], parts[0])
        else:
            print("Uso incorrecto del comando /ban. Debe ser /ban nickname #channel")
        continue
    if message.startswith("/unban"):
        # Asume que el comando tiene el formato "/unban nickname #channel"
        parts = message[7:].split(' ')
        if len(parts) == 2:
            unban_user(parts[1], parts[0])
        else:
            print("Uso incorrecto del comando /unban. Debe ser /unban nickname #channel")
        continue
    if message.startswith("/list"):
        list_channels()
        continue
    if message.startswith("/userhost "): # el estado de conexión (indicado por el signo más +), el modo de usuario (indicado por el tilde ~), el nombre de usuario real (en este caso, "miUsuario"), y el hostname o dirección IP del usuario (e756-a214-b931-5050-47f1.206.152.ip).
        nicknames = message[10:].split()
        userhost_query(nicknames)
        continue
    if message.startswith("/wallops "): # solo para operadores
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
print("exit")
irc.close()
