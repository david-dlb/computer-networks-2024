import socket
import threading


# **************************************************************************
#                               CREDENCIALES
# **************************************************************************

# server_ip = input("Ingrese la dirección IP del servidor: ")
# port = int(input("Ingrese el puerto: "))
# channel = input("Ingrese el nombre del canal a unirse")
# nickname = input("Ingrese su apodo: ")
# realname = input ("Ingrese 1 para usar conexión segura. Ingrese 2 para el caso contrario: ")
# password = input("Ingrese su contraseña")

# Solicitar al usuario que ingrese los 6 valores en una sola línea
input_values = input("Ingrese los 6 valores separados por espacios: ")

# Dividir la cadena de entrada en una lista de valores
values_list = input_values.split()

# Ahora puedes acceder a cada valor por su índice en la lista
server = values_list[0]
portStr = int(values_list[1])
channel = values_list[2]
nickname = values_list[3]
realname = values_list[4]
password = values_list[5]

# Asegurarse de que el puerto sea un entero
port = int(portStr)

print(f"Servidor: {server}")
print(f"Puerto: {port}")
print(f"Canal: {channel}")
print(f"Apodo: {nickname}")
print(f"Nombre real: {realname}")
print(f"Contraseña: {password}")





# *************************************************************************
#                             FUNCIONALIDADES
# *************************************************************************

# Enviar el mensaje a todos los usuarios del canal
def send_channel_message(message):
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))

# Mandar un mensaje por privado a un usuario
def send_private_message(nickname, message):
    print(f'Enviando mensaje privado a {nickname}')
    irc.send(bytes(f'PRIVMSG {nickname} :{message}\r\n', 'UTF-8'))

# Salir del cliente
def quit_irc():
    irc.send(bytes('QUIT\r\n', 'UTF-8'))
    irc.close()
    print("Desconectado del servidor IRC.")

# Enviar una noticia
def send_notice(target, message):
    irc.send(bytes('NOTICE ' + target + ' :' + message + '\r\n', 'UTF-8'))

# Invitar un usuario a un canal
def invite_user(nickname, channel):
    irc.send(bytes('INVITE ' + nickname + ' ' + channel + '\r\n', 'UTF-8'))

# Mostrar tema de conversacion en un canal
def topic(channel):
    irc.send(bytes('TOPIC ' + channel + '\r\n', 'UTF-8'))

# Definir tema de conversacion en un canal (en el que estas)
def set_topic(channel, new_topic):
    irc.send(bytes('TOPIC ' + channel + ' :' + new_topic + '\r\n', 'UTF-8'))

# Mostrar info de un usuario especifico online
def whois_user(nickname):
    irc.send(bytes('WHOIS ' + nickname + '\r\n', 'UTF-8'))

# Mostrar info de un usuario especifico no online
def whowas_user(nickname):
    irc.send(bytes('WHOWAS ' + nickname + '\r\n', 'UTF-8'))

# Mostrar info de todos los usuarios online
def who_channel(channel):
    irc.send(bytes('WHO ' + channel + '\r\n', 'UTF-8'))

# Modificar nickname
def change_user():
    new_nickname = input("Ingrese el nuevo nombre de usuario: ")
    global nickname 
    nickname = new_nickname
    irc.send(bytes('NICK ' + new_nickname + '\r\n', 'UTF-8'))

# Info general del servidor
def stats():
    irc.send(bytes('STATS' + '\r\n', 'UTF-8'))

# Eliminar un usuario de un canal
def part_channel():
    global channel # Asegúrate de que puedas modificar la variable global
    if channel: # Verifica que el canal no esté vacío
        irc.send(bytes('PART ' + channel + '\r\n', 'UTF-8'))
    else:
        print("No hay un canal al que unirse.")

# Listar los usuarios de un canal
def list_names():
    irc.send(bytes('NAMES ' + channel + '\r\n', 'UTF-8'))

# Listar los canales en el servidor
def list_channels():
    irc.send(bytes('LIST\r\n', 'UTF-8'))

# Servidores disponibles
def list_connected_servers():
    irc.send(bytes('LINKS\r\n', 'UTF-8'))

# Unirse a un canal
def join_channel(channel_name):
    global channel
    # Asegúrate de que el nombre del canal no esté vacío
    if channel_name:
        irc.send(bytes('JOIN ' + channel_name + '\r\n', 'UTF-8'))
        channel = channel_name
    else:
        print("El nombre del canal no puede estar vacío.")

# Abandonar un canal
def part_channel():
    global channel
    if channel: # Verifica que el canal no esté vacío
        irc.send(bytes('PART ' + channel + '\r\n', 'UTF-8'))
        print(f"Has abandonado el canal {channel}.")
        channel = '' # Limpia el nombre del canal para indicar que no estás en un canal
    else:
        print("No estás en un canal para abandonar.")

# Sacar un usuario de un canal
def kick_user(nickname):
    irc.send(bytes('KICK ' + channel + ' ' + nickname + ' :You are kicked!\\r\\n', 'UTF-8'))
    send_channel_message('KICK ' + channel + ' ' + nickname + ' :You are kicked!\\r\\n')

# El usuario no puede volver a entrar en el canal
def ban_user(channel, nickname):
    # Asegúrate de que el canal y el nickname no estén vacíos
    if channel and nickname:
        irc.send(bytes(f'MODE {channel} +b {nickname}\r\n', 'UTF-8'))
    else:
        print("El canal y el nickname no pueden estar vacíos.")

# El usuario puede volver a entrar al canal
def unban_user(channel, nickname):
    # Asegúrate de que el canal y el nickname no estén vacíos
    if channel and nickname:
        irc.send(bytes(f'MODE {channel} -b {nickname}\r\n', 'UTF-8'))
    else:
        print("El canal y el nickname no pueden estar vacíos.")





# *************************************************************************
#                           MANEJAR LA ESCUCHA
# *************************************************************************

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
            print(' ')
            print('data : '+ data)
            print(' ')

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

            # # Desglosar data para procesarla
            # dataArr = data.split(' ')

            # # Manejar cuando un usuario se une a un canal
            # if 'JOIN' in dataArr:
            #     userJoin = dataArr[0].split('!',1)[0]
            #     if userJoin != 'rs:':
            #         print(f'El usuario {userJoin} se ha unido al canal')

            # # Manejar cuando un usuario se va del servidor
            # if ':Quit:' in dataArr:
            #     index_user = 0
            #     for i in range(len(dataArr) - 1): # buscar data a quien es mandado el smsa  (a un usuario o un canal)
            #         if dataArr[i] == ':Quit:':
            #             index_user = i+1
            #             break
            #     print(f'El usuario {dataArr[index_user]} ha abandonado el servidor')

            # # Manejar el recibir un mensaje
            # if 'PRIVMSG' in dataArr:
            #     words = dataArr
            #     user_from = dataArr[0].split('!',1)[0] # seleccionar el usuario que mando el sms
            #     index_msgTarget = 0
            #     for i in range(len(dataArr) - 1): # buscar data a quien es mandado el smsa  (a un usuario o un canal)
            #         if dataArr[i] == 'PRIVMSG':
            #             index_msgTarget = i+1
            #             break
            #     msg = ' '.join(dataArr[(index_msgTarget+1):])
            #     if dataArr[index_msgTarget].startswith('#'):
            #         print(f'<{user_from}> send to channel {dataArr[index_msgTarget]} : {msg}')
            #     elif dataArr[index_msgTarget] == nickname:
            #         print(f'<{user_from}> send pv {dataArr[index_msgTarget]} : {msg}')

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






# *************************************************************************
#                             OTRAS FUNCIONES
# *************************************************************************

def userhost_query(nicknames):
    nicknames_str = ' '.join(nicknames)
    irc.send(bytes('USERHOST ' + nicknames_str + '\r\n', 'UTF-8'))

def wallops_message(message):
    irc.send(bytes('WALLOPS :' + message + '\r\n', 'UTF-8'))

def send_action():
    action = input("action: ")
    irc.send(bytes('PRIVMSG ' + channel + ' :\x01ACTION ' + action + '\x01\r\n', 'UTF-8'))

def connect_to_server(server_name):
    # Asegúrate de que el nombre del servidor no esté vacío
    if server_name:
        irc.send(bytes(f'SERVER {server_name}\r\n', 'UTF-8'))
    else:
        print("El nombre del servidor no puede estar vacío.")

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






# *************************************************************************
#                            DICCIONARIO DE AYUDA
# *************************************************************************

# Lista de diccionarios con los comandos disponibles, sus descripciones y ejemplos de uso
comandos_ayuda = [
    {"comando": "/msgpv", "descripcion": "Envía un mensaje privado a un usuario específico.", "ejemplo": "/msgpv nickname mensaje"},
    {"comando": "/whois", "descripcion": "Muestra información sobre un usuario específico.", "ejemplo": "/whois nickname"},
    {"comando": "/whowas", "descripcion": "Muestra información sobre un usuario que ya no está en línea.", "ejemplo": "/whowas nickname"},
    {"comando": "/list", "descripcion": "Muestra una lista de canales disponibles en el servidor.", "ejemplo": "/list"},
    {"comando": "/names", "descripcion": "Muestra los nombres de usuario en el canal actual.", "ejemplo": "/names"},
    {"comando": "/notice", "descripcion": "Envía una notificación a un usuario o canal.", "ejemplo": "/notice nickname mensaje"},
    {"comando": "/ban", "descripcion": "Banea a un usuario de un canal.", "ejemplo": "/ban nickname #canal"},
    {"comando": "/unban", "descripcion": "Desbanea a un usuario de un canal.", "ejemplo": "/unban nickname #canal"},
    {"comando": "/op", "descripcion": "Otorga el estado de operador a un usuario en el canal actual.", "ejemplo": "/op nickname"},
    {"comando": "/deop", "descripcion": "Revoca el estado de operador de un usuario en el canal actual.", "ejemplo": "/deop nickname"},
    {"comando": "/who", "descripcion": "Muestra información sobre los usuarios en un canal.", "ejemplo": "/who #canal"},
    {"comando": "/links", "descripcion": "Muestra los servidores conectados.", "ejemplo": "/links"},
    {"comando": "/nick", "descripcion": "Cambia el nombre de usuario del cliente.", "ejemplo": "/nick nuevoNickname"},
    {"comando": "/stats", "descripcion": "Solicita estadísticas sobre el servidor o un objeto específico.", "ejemplo": "/stats"},
    {"comando": "/join", "descripcion": "Permite unirse a un canal específico.", "ejemplo": "/join #canal"},
    {"comando": "/kick", "descripcion": "Expulsa a un usuario de un canal.", "ejemplo": "/kick nickname #canal"},
    {"comando": "/invite", "descripcion": "Invita a un usuario a un canal.", "ejemplo": "/invite nickname #canal"},
    {"comando": "/quit", "descripcion": "Cierra la conexión del cliente con el servidor.", "ejemplo": "/quit"},
    {"comando": "/topic", "descripcion": "Muestra o cambia el tema del canal.", "ejemplo": "/topic #canal nuevoTema"},
    {"comando": "/part", "descripcion": "Permite abandonar el canal actual.", "ejemplo": "/part"},
]




# *************************************************************************
#                            INICIAR LA CONEXION
# *************************************************************************

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






# *************************************************************************
#                                     MAIN
# *************************************************************************

while True:
    message = input()
    

    
#                           IMPLEMENTADOS Y TESTEADOS
# --------------------------------------------------------------------------

    if message.startswith("/help"):
        print("Comandos disponibles:")
        for comando in comandos_ayuda:
            print(f"{comando['comando']}: {comando['descripcion']} Ejemplo: {comando['ejemplo']}")
            print(' ')
        continue

    if message.startswith("/msgpv"):
        # Asume que el comando tiene el formato "/msgpv nickname msg"
        msg = message[7:].split(' ', 1)
        send_private_message(msg[0], msg[1])
        continue
    
    if message.startswith("/whois "):
        whois_user(message[7:])
        continue
    
    if message.startswith("/whowas "):
        whowas_user(message[8:])
        continue
    
    if message.startswith("/list"):
        list_channels()
        continue
    
    if message.startswith("/names"):
        list_names()
        continue
    
    if message.startswith('/notice'):
        msgarr = message.split(' ', 2)
        send_notice(msgarr[1], msgarr[2])
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
    
    if message.startswith("/who "):
        who_channel(message[5:])
        continue
    
    if message.startswith("/links"):
        list_connected_servers()
        continue
    
    if message.startswith("/nick "):
        change_user()
        continue
    
    if message.startswith("/stats"):
        stats()
        continue
    
    if message.startswith("/join"):
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
    
    if message.startswith("/topic"):
        parts = message.split(' ')
        if len(parts) == 2:
            # Asume que el comando tiene el formato /topic #canal
            topic(parts[1])
            continue
        elif len(parts) > 2:
            # Extraer el canal y el nuevo tema del mensaje
            parts = message[7:].split(' ', 1) # Asume que el comando tiene el formato "/topic #canal Nuevo tema del canal"
            if len(parts) == 2:
                channel_name, new_topic = parts
                set_topic(channel_name, new_topic)
            continue
        print("Uso incorrecto del comando /topic. Debe ser /topic #canal Nuevo tema del canal")
        continue
    
    if message.startswith("/part"):
        part_channel()
        continue





#                       IMPLEMENTADOS PERO NO TESTEADOS
# -------------------------------------------------------------------------

    if message.startswith("/server"):
        # Asume que el comando tiene el formato "/server server_name"
        server_name = message[8:]
        connect_to_server(server_name)
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
    
    if message.startswith("/userhost "): # el estado de conexión (indicado por el signo más +), el modo de usuario (indicado por el tilde ~), el nombre de usuario real (en este caso, "miUsuario"), y el hostname o dirección IP del usuario (e756-a214-b931-5050-47f1.206.152.ip).
        nicknames = message[10:].split()
        userhost_query(nicknames)
        continue
    
    if message.startswith("/wallops "): # solo para operadores
        wallops_message(message[9:])
        continue
    
    if message.startswith("/users"):
        list_users(channel)
        continue
    
    if message.startswith("/action "):
        send_action(message[8:])
        continue



    # ENVIAR UN SMS A TODOS POR DEFAULT
    send_channel_message(message)

print("exit")
irc.close()
