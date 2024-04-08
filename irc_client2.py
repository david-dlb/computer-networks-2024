import socket
import threading

def send_message(message):
    irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))

def quit_irc():
    irc.send(bytes('QUIT\r\n', 'UTF-8'))
    irc.close()
    print("Desconectado del servidor IRC.")

def invite_user(nickname, channel):
    irc.send(bytes('INVITE ' + nickname + ' ' + channel + '\r\n', 'UTF-8'))

def set_topic(new_topic):
    irc.send(bytes('TOPIC ' + channel + ' :' + new_topic + '\r\n', 'UTF-8'))

def send_action():
    action = input("action: ")
    irc.send(bytes('PRIVMSG ' + channel + ' :\x01ACTION ' + action + '\x01\r\n', 'UTF-8'))

def listen_for_messages():
    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print(data)
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

def handle_error(error_message):
    print("Error recibido del servidor:", error_message)
    # Aquí puedes implementar lógica adicional para manejar el error, como intentar reconectar o mostrar un mensaje al usuario.

server = 'irc.dal.net'
port = 6667
channel = '#miCanal'
nickname = 'miUsuario1'
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
    if message.startswith("/action "):
        send_action(message[8:])
        continue
    if message.startswith("/topic "):
        set_topic(message[7:])
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
