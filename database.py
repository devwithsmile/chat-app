from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydb = client['chatapp']
mycollection = mydb['Signup']

my_data = mydb['signup']

session_details=mydb['session_details']


def user_info(username, password):
    my_data.insert_one({"username": username, "password": password})


def save_user(name, room, message):
    mycollection.insert_one({"name": name, "room": room, "message":message})


def get_user(username1):
    x = my_data.find_one({"username": username1})
    return x


def get_password(password):
    y = my_data.find_one({"password": password})
    return y


def save_user_session1(user,time_in):
    x=session_details.insert_one({"username":user,"time_in":time_in,"time_out":'0',"current_room":'0'})


def save_user_session2(current_room):
    y = {"current_room": "0"}
    y1 = {"$set":{"current_room": current_room}}
    session_details.update_one(y, y1)


def save_user_session3(username,session,time_out):
    print(session)

    #its a wrong logic but leaving it for now its changing the first occurence of 0 instead of the exact same user it logged in, got it?
    if session['name'] == username:
        time_out = str(time_out)
        print("time out in save session", time_out)
        x = {"time_out": "0"}
        x1 = {"$set": {"time_out": time_out}}
        session_details.update_one(x, x1)
        print("time out save done ")
    else:
        print("user not in session m in sus3")