from flask import Flask, render_template, request , redirect, url_for
from flask_socketio import SocketIO
import db

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/report')
def report():
    data = db.show_data()
    print(data)
    return render_template('report.html', data=data)



if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)