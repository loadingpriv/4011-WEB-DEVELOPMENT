from flask import Flask, render_template, request, session, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random 


app = Flask(__name__)
app.config['SECRET_KEY'] =  'dontgoclasslol'
socketio = SocketIO(app)

if __name__ =="__main__":
    socketio.run(app, debug=True) 