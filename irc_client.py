import socket

def irc_client():
    server = 'irc.dal.net'
    channel = '#miCanal'
    nickname = 'miUsuario'

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, 6667))
    irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
    irc.send(bytes('USER ' + nickname + ' 0 * :' + nickname + '\r\n', 'UTF-8'))
    irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

    while True:
        message = irc.recv(2048).decode('UTF-8')
        if message.startswith('PING'):
            irc.send(bytes('PONG :' + message.split(':')[1] + '\r\n', 'UTF-8'))
        elif 'PRIVMSG' in message:
            print(message)

if name == 'main':
    irc_client()