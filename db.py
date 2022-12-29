from bson import ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
mydata = client['chatapp']
mycol = mydata['session_details']


# def insert_employee_details(Employee_Name, Email, Mobile, Salary, department):
#     record = mycol.insert_one({'EmployeeName':Employee_Name, 'Email':Email , 'Mobile':Mobile, 'salary':Salary, 'Department':department})

def show_data():
    AllData = []
    data = mycol.find({},{})
    for i in data:
        i['_id'] = str(ObjectId(i['_id']))
        AllData.append(i)
    return AllData


# def edit(data):
#     edit_data = mycol.find_one({'_id':ObjectId(data)})
#     edit_data['_id'] = str(ObjectId(edit_data['_id']))
#     return edit_data



# def update_data(id, Emp, email, mobile, salary, dept):
#     update = mycol.update_one({'_id':ObjectId(id)}, {'$set': {'EmployeeName': Emp, 'Email': email, 'Mobile': mobile, 'salary': salary, 'Department': dept}})

#print(show_data())
#print(edit('62d4e99f14995ccfeb0bc315'))
