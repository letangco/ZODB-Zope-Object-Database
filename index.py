from ZODB import DB
import uuid
from ZODB.FileStorage import FileStorage
from ZODB.PersistentMapping import PersistentMapping
from Persistence import Persistent
import transaction
class Employee(Persistent):
    def __init__(self, _id, name, manager=None):
        self._id = _id
        self.name = name
        self.manager = manager

# set up the database
storage = FileStorage("data.fs")
db=DB(storage)
connection=db.open()
root=connection.root()

# get the employees mapping, creating an empty mapping if
# necessary
if 'employees' not in root.keys():
    root["employees"] = {}
employees = root["employees"]
def listEmployees():
    if len(employees.values())==0:
        print('There are no employees.', root)
        print
        return
    print('                  id                  |  name|manager')
    print
    for employee in employees.values():
        # print("Name: %s" % employee.name)
        if employee.manager is not None:
            # print("Manager's name: %s" % employee.manager)
            print(employee._id, ' | ',employee.name, employee.manager)
            print
        else:
            print(employee._id, ' | ',employee.name)
            print
        
def addEmployee(_id, name, manager_name=None):
    if name in employees.keys():
        print("There is already an employee with this name.")
        return
    if manager_name:
        try:
            # manager = employees[name]
            print('in manager: ', manager_name)
            employees[_id]=Employee(_id, name, manager_name)
        except KeyError:
            print
            print("No such manager")
            print
            return
        # employees[name]=Employee(name, manager)
    else:
        employees[_id]=Employee(_id, name)
    print('employee: ', employees)
    root['employees'] = employees #reassign to change
    transaction.commit()
    print("Employee %s added." % name)
    print


def UpdateInfoEmp(_id, name, manager):
    try:
        print('hasEmp: ', employees[_id])
    except KeyError:
        print
        print("No such employee")
        print
        return
    employees[_id]=Employee(_id, name, manager)
    print("Employee %s updated." % _id)
    print
    root["employees"] = employees
    transaction.commit()

def deleteEmployee(_id):
    try:
        print('hasEmp: ', employees[_id])
    except KeyError:
        print
        print("No such employee")
        print
        return
    del employees[_id]
    print("Employee %s deleted." % _id)
    print
    root["employees"] = employees
    transaction.commit()

if __name__=="__main__":
    while 1:
        choice=input("Press 'L' to list employees, 'A' to add an employee, 'U' to update an employee by id, 'D' to delete an employee by id or 'Q' to quit:")
        choice=choice.lower()
        if choice=="l":
            listEmployees()
        elif choice=="a":
            name=input("Employee name: ")
            manager_name=input("Manager name: ")
            current_employee = Employee(str(uuid.uuid1()), name, manager_name)
            addEmployee(current_employee._id, current_employee.name, current_employee.manager)
        elif choice=="u":
            _id=input("Id Employee update: ")
            name=input("Employee name: ")
            manager_name=input("Manager name: ")
            UpdateInfoEmp(_id, name, manager_name)
        elif choice=="d":
            _id=input("Id Employee delete: ")
            deleteEmployee(_id)
        elif choice=="q":
            break
    # close database
    connection.close()