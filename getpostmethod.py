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

# @app.route('/details' , methods=['GET', 'POST'])
# def details():
#     if request.method == 'POST':
#         Employee_Name = request.form.get('username')
#         Email = request.form.get('email')
#         Mobile = request.form.get('Number')
#         Salary = request.form.get('salary')
#         department = request.form.get('departmentId')
#         db.insert_employee_details(Employee_Name, Email, Mobile, Salary, department)
#     return redirect(url_for('home'))


# @app.route('/update', methods=['GET', 'POST'])
# def update():
#     if request.method=='POST':
#         Emp = request.form.get('updateusername')
#         email = request.form.get('updateemail')
#         mobile = request.form.get('updatemobile')
#         salary = request.form.get('updatesalary')
#         dept = request.form.get('updateDepartment')
#         id = request.form.get('id')
#         db.update_data(id,Emp, email, mobile, salary, dept)
#     return redirect(url_for('home'))

# @socketio.on('datatable')
# def handle_data(data):
#
#     record = db.edit(data)
#
#     socketio.emit('recive_data', record)


if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)