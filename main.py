from flask import Flask, render_template , request, session, url_for, redirect
from flask_socketio import join_room, leave_room, send, SocketIO
import random 
from string import ascii_uppercase


app = Flask(__name__)
app.config['SECRET_KEY'] =  'dontgoclasslol2024'
socketio = SocketIO(app)

rooms = {}


def generate_unique_code(Length):
    while True:
        code = ""
        for _ in range (Length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    return code

@app.route('/', methods = ['POST','GET'])
def home():
    session.clear()
    if request.method == "POST":
        code = request.form.get("code")
        name = request.form.get("name")
        join = request.form.get("join" , False)
        create =request.form.get("create", False)


        if not name:
            print("Not Name")
            return render_template("home.html", error="PLEASE ENTER NAME." ,code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", error="PLEASE ENTER PMC CODE.",code=code, name=name)
        
        room = code 
        if create != False:
            room = generate_unique_code(4)
            rooms[room]= {"members": 0, "messages":[]}

        elif code not in rooms:
            return render_template("home.html", error="PMC ROOM DOES NOT EXIST.",code=code, name=name)
        

        
        session["name"]= name 
        session["room"]= room
        return redirect(url_for("room"))
        
        return render_template("home.html")



    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home") )


    return render_template("room.html",code=room)


@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send (content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    name = session.get("name")
    room = session.get("room")
    if not room or not name:
        return 
    if room not in rooms:
        return
    
    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room] ["members"] += 1
    print(f"{name} joined PMC {room}")


@socketio.on("disconnect")
def disconnect():
    name = session.get("name")
    room = session.get("room")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1 
        if room [room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name}has left the room {room} ")


if __name__ =="__main__":
    socketio.run(app, debug=True) 