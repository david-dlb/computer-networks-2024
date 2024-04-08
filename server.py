from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import socket

app = Flask(__name__)
socketio = SocketIO(app)

# Configuración del servidor IRC
server = 'irc.dal.net'
port = 6667
channel = '#miCanal'
nickname = 'miUsuario3'
realname = 'Mi Nombre Real3'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

def reconnect_irc():
    global irc
    irc.close() # Cierra el socket actual
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Crea un nuevo socket
    irc.connect((server, port)) # Intenta reconectar
    irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
    irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
    irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))



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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    if message:
        try:
            irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))
            return {'status': 'success'}, 200
        except BrokenPipeError:
            print("La conexión con el servidor IRC se ha perdido. Reconectando...")
            reconnect_irc() # Asegúrate de que esta función esté definida para reconectar
            return {'status': 'reconnected'}, 200
        except Exception as e:
            print("Error inesperado:", e)
            return {'error': 'Error sending message'}, 500
    else:
        return {'error': 'No message provided'}, 400

if __name__ == '__main__':
    # Inicia el hilo para escuchar el servidor IRC
    thread = threading.Thread(target=listen_for_messages)
    thread.start()
    socketio.run(app)
