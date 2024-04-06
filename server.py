from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import socket

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet')

# Configuración del servidor IRC
server = 'irc.dal.net'
port = 6667
channel = '#miCanal'
nickname = 'miUsuario'
realname = 'Mi Nombre Real'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))
irc.send(bytes('NICK ' + nickname + '\r\n', 'UTF-8'))
irc.send(bytes('USER ' + nickname + ' 0 * :' + realname + '\r\n', 'UTF-8'))
irc.send(bytes('JOIN ' + channel + '\r\n', 'UTF-8'))

def listen_irc():
    while True:
        try:
            data = irc.recv(2048).decode('utf-8')
            print("Datos recibidos del servidor IRC:", data)
            if data.find('PRIVMSG') != -1:
                # Extrae el mensaje del servidor IRC
                message = data.split('PRIVMSG')[1].split(':', 1)[1]
                # Emite el mensaje a todos los clientes conectados
                socketio.start_background_task(emit, 'new_message', {'message': message})
        except Exception as e:
            print("Error al recibir datos:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    if message:
        irc.send(bytes('PRIVMSG ' + channel + ' :' + message + '\r\n', 'UTF-8'))
        return {'status': 'success'}, 200
    else:
        return {'error': 'No message provided'}, 400

if __name__ == '__main__':
    # Inicia el hilo para escuchar el servidor IRC
    threading.Thread(target=listen_irc).start()
    socketio.run(app)
