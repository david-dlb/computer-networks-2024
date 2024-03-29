import socket
server = 'irc.dal.net'
port = 6667
channel = '#miCanal'
nickname = 'miUsuario2'
realname = 'Mi Nombre Real2'



def irc_client():

    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, port))
    irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
    irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
    irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))
    def send_message(message):
        irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))

    while True:
        try:
            data = irc.recv(2048).decode('UTF-8')
            print(data)
            sender = data.split('!', 1)[0][1:]

            send_message('como ta mi hermano, ' + sender + '!')

            if data.find('PING') != -1:
                irc.send(bytes('PONG ' + data.split()[1] + '\r\n', 'UTF-8'))

            if data.find('PRIVMSG') != -1:
                sender = data.split('!', 1)[0][1:]
                message = data.split('PRIVMSG', 1)[1].split(':', 1)[1]

                if message.strip() == '!hello':
                    send_message('Hello, ' + sender + '!')

            if data.find('JOIN') != -1:
                joined_user = data.split('!')[0][1:]
                send_message('Welcome, ' + joined_user + '!')

            if data.find('QUIT') != -1:
                quit_user = data.split('!')[0][1:]
                send_message('Goodbye, ' + quit_user + '!')
        except OSError as e:
            print("Error:", e)
            break

    irc.close()

if __name__ == '__main__':
    irc_client()
