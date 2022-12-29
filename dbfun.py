import pymongo
from flask import request
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room
from flask_session import Session
# using datetime module

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = my_client["chatapp"]
my_chat = mydb["all_chat"]
my_users = mydb["all_users"]
my_details = mydb['session_details']

app = Flask(__name__)
socketio = SocketIO(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@app.route('/dbv')
def dbv():
    keys = []
    for x in my_details.find():
        keys.append(x.keys())
        th=list(keys[0])
        print(th[0])
        print(type(th))
        num = (len(keys))

        stringa = " ".join([str(item) for item in th])
        print('this is stringa',stringa)

    return render_template('datatable.html', num=num, th=stringa)




if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)


