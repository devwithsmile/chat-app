import pymongo
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room
from database import get_user, user_info, get_password, save_user_session1, save_user_session2, \
    save_user_session3
from flask_session import Session
# using datetime module
import datetime
import db
import getpostmethod


app = Flask(__name__)
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["chatapp"]
my_rooms = mydb["all_rooms"]
my_users = mydb["all_users"]
my_chat = mydb['all_chat']
my_broadcastedmsgs = mydb["broadcastedmsgs"]


@app.route('/')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    messages = ''
    if request.method == 'POST':

        username1 = request.form.get('username')
        password = request.form.get('password')

        if get_user(username1) == None:
            user_info(username1, password)
            return redirect(url_for('login'))
        else:
            messages = 'user already exist'
    return render_template('signup.html', messages=messages)


@socketio.on('/loginpage')
@app.route('/login', methods=['POST', 'GET'])
def login():
    note = ''
    if request.method == 'POST':
        username = request.form.get('username')

        session['name'] = request.form.get('username')
        #get time and give a stamp
        ct = datetime.datetime.now()
        ts = ct.timestamp()
        #saving session half detail
        save_user_session1(username, ct)
        password = request.form.get('password')
        if get_user(username) != None and get_password(password) != None:
            return redirect(url_for('index'))
        else:
            note = 'username or password should be wrong'

    return render_template('login.html', note=note)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():

    time_out = datetime.datetime.now()
    username=session['name']
    save_user_session3(username, session, time_out)
    session["name"] = None
    print("getting out of session")
    return render_template('signup.html')

rooms = []
usernames = []
for x in my_chat.find({}, {"_id": 0, "room": 1}):
    rooms.append(x['room'])


for x in my_users.find({}, {"_id": 0, "user": 1}):
    usernames.append(x['user'])


@app.route('/chat')
def chat():
    print('inside chat function')
    # username = request.args.get('username')
    room = request.args.get('room')
    username = session['name']
    session['room'] = room
    print("room id of user is: ",session['room'])
    save_user_session2(room)
    #print("username by session is: ", username)
    room_cnt = rooms.count(room)
    uname_cnt = usernames.count(username)

    if room_cnt > 0 and uname_cnt > 0:
        return render_template('chat.html', username=username, room=room)

    elif room_cnt == 0 and uname_cnt > 0:
        rooms.append(room)
        add_room_query = {"room": room}
        xk = my_rooms.insert_one(add_room_query)
        print("new room created:", xk)
        return render_template('chat.html', username=username, room=room)

    elif uname_cnt == 0 and room_cnt > 0:
        usernames.append(username)
        add_user_query = {"user": username}
        xk = my_users.insert_one(add_user_query)
        print("new user created:", xk)
        return render_template('chat.html', username=username, room=room)
    elif uname_cnt == 0 and room_cnt == 0:
        # user_add
        usernames.append(username)
        add_user_query = {"user": username}
        y = my_users.insert_one(add_user_query)
        print("new user created:", y)

        # room_add
        rooms.append(room)
        add_room_query = {"room": room}
        xk = my_rooms.insert_one(add_room_query)
        print("new room created:", xk)
        return render_template('chat.html', username=username, room=room)
    else:
        print("inside else of chat function")
        return render_template("index.html")


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'], data['room'], data['message']))

    # dev's code
    add_chat_query = {"room": data['room'], "username": data['username'], "message": data['message']}
    z = my_chat.insert_one(add_chat_query)
    print("new chat added:", z)

    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    #ct
    ct = datetime.datetime.now()
    save_user_session2(data['room'])
    save_user_session3(session['name'],session,ct)
    socketio.emit('leave_room_announcement', data, room=data['room'])
    return render_template('index.html')


@socketio.on('broadcasting')
def broadcasting(data):
    print("inside broadcasting or broad function")
    # dev's code
    add_chat_query = {"message": data}
    z = my_broadcastedmsgs.insert_one(add_chat_query)
    print("new msg broadcasted:", z)
    print("going to emit", data)
    data = "broadcasted msg:"+str(data)
    
    socketio.emit('rb', data)
    print("emitted broadcast")

fprevdata=[]


@socketio.on("prev_room_chat")
def prev_room_chat(data):
    print("previous chat: ",data)
    print("its datat-type",type(data))
    room_id=session['room']
    print(str(room_id)+ "in prev chat room")
   
    my_doc = my_chat.find({"room":room_id})
    if my_doc == None:
        pass
    else:
        for z in my_doc:
            data = str("<b>" + z['username']) + "</b>" + ":" + str(z['message'])
            fprevdata.append(str(data) + "\n")

            print("mangane k baad: ", data)
            print("m k baad: ", type(data))
            conv = '<br>'.join([str(item) for item in fprevdata])
            print("final data: " + conv)

            socketio.emit("set_room_chat", conv)


@app.route('/database')
def databaseview():

    for x in my_users.find({}, {"_id": 0, "user": 1}):
        td=""
        td=td+str(x['user'])
        print('hey here with td: ',td)
        # usernames.append(x['user'])


    return render_template('datatable.html',thead="table's head",th="th tag",td1=td)


@app.route('/report')
def report():
    data = db.show_data()
    print(data)
    return render_template('report.html', data=data)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
