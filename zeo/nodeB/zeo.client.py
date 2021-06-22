from ZEO.ClientStorage import ClientStorage
from ZODB import DB
import ZEO
import ZODB.config
from Persistence import Persistent
import shortuuid
import ZODB.tests.util, transaction

CONSTANTS_DEPARTMENT = 'DEPARTMENTS'
CONSTANTS_EMPLOYEE = 'EMPLOYEES'

class Department(Persistent):
  def __init__(self, _idDept, nameDept):
    self._idDept = _idDept
    self.nameDept = nameDept
class Employee(Persistent):
  def __init__(self, _idEmp, name, _idDept, salary):
    self._idEmp = _idEmp
    self.name = name
    self._idDept = _idDept
    self.salary = salary
  
  def __update_info__(self, _idEmp, name, _idDept, salary):
    self._idEmp = _idEmp
    if (bool(name)):
      self.name = name
    if (bool(_idDept)):
      self._idDept = _idDept
    if (bool(salary)):
      self.salary = salary

print("############starting client################")

# connection = ZEO.connection(('localhost',8090))
# root = connection.root()
# db_departments = root[CONSTANTS_DEPARTMENT]


storage=ClientStorage(('localhost',8090))
db=DB(storage)
conn=db.open()
print("connection opened")
root=conn.root()
print("established connection")
if CONSTANTS_DEPARTMENT not in root.keys():
  root[CONSTANTS_DEPARTMENT] = {}
db_departments = root[CONSTANTS_DEPARTMENT]

# transaction.commit()
# print(department)
print('#############################')
tm_client = transaction.TransactionManager()
db = ZODB.config.databaseFromURL('./test.config')
conn = db.open(transaction_manager=tm_client)
client_db = conn.root()

if CONSTANTS_EMPLOYEE not in client_db.keys():
  client_db[CONSTANTS_EMPLOYEE] = {}
employees = client_db[CONSTANTS_EMPLOYEE]


def addEmployee(_idEmp, name, _idDept, salary):
  _list_Id_Depart = db_departments.keys()
  if _idDept in _list_Id_Depart:
    print('=>>>EMPLOYEE: ', _idEmp, ' - ', name, ' - ', _idDept, ' - ', salary)
    employees[_idEmp] = Employee(_idEmp, name, str(_idDept), salary)
    print('Success: 200, Add Employee successfull.')
    print
  else:
    print('Error: 404, Department Id not exist!.')
    print
  client_db[CONSTANTS_EMPLOYEE] = employees
  tm_client.commit()

def __list_employee_mapping():
  if len(employees.values()) == 0:
    print('There are no employee.', client_db)
    print
    return
  print('###############LIST EMPLOYEE#################')
  for item in employees.values():
    print(item._idEmp, ' | ', item.name, ' | ', item._idDept , ' | ', db_departments[item._idDept].nameDept, ' | ', item.salary)
    print

def __delete_employee_by_id(id):
  _mapping_id_employee = employees.keys()
  if id in _mapping_id_employee:
    __confirm = input('Do you want delete employee? (Y/N)')
    if __confirm.lower() == 'y':
      del employees[id]
      client_db[CONSTANTS_EMPLOYEE] = employees
      tm_client.commit()
      print('Employee %s has deleted.!' % id)
    else:
      print('Exit delete program!')
  else:
    print('Not Exist Id Employee!')

def __update_employee_by_id__(id, data):
  _mapping_id_employee = employees.keys()
  if id in _mapping_id_employee:
    print(employees[id].name)
    tempEmp = Employee(id, employees[id].name, employees[id]._idDept, employees[id].salary)
    tempEmp.__update_info__(id, data['name'], data['_idDept'], data['salary'])
    __confirm = input('Do you want update employee? (Y/N)')
    if __confirm.lower() == 'y':
      employees[id] = tempEmp
      client_db[CONSTANTS_EMPLOYEE] = employees
      tm_client.commit()
      print('Employee %s has updated.!' % id)
    else:
      print('Exit update program!')
  else:
    print('Not Exist Id Employee!')

# main program
if __name__ == '__main__':
  while 1:
    print('#########MENU###########')
    print('# LD. LIST DEPARTMENT  #')
    print('# A. ADD EMPLOYEE      #')
    print('# L. LIST EMPLOYEE     #')
    print('# D. DELETE EMPLOYEE   #')
    print('# U. UPDATE EMPLOYEE   #')
    print('# Q. QUICK PROGRAM     #')
    print('########################')
    options = input('Select a option: ')
    options = options.lower()
    if options == 'a':
      name=input("Employee name: ")
      dept_name=input("Department Id: ")
      salary = input('Salary: ')
      addEmployee(str(shortuuid.uuid()), name, dept_name, salary)
    elif options == 'l':
      __list_employee_mapping()
    elif options == 'd':
      _id_employee = input('Id of employee: ')
      __delete_employee_by_id(_id_employee)
    elif options == 'u':
      _id_employee = input('Id of employee: ')
      data = {}
      if bool(_id_employee) == True:
        _name_employee = input('Name of employee: ')
        _id_department = input('Id Department: ')
        _salary = input('Salary: ')
        data['name'] = _name_employee
        data['_idDept'] = _id_department
        data['salary'] = _salary
      else: print('Id invalid!!!')
      __update_employee_by_id__(_id_employee, data)
    elif options == 'ld':
      print('#######LIST DEPARTMENT#######')
      print('______________________id|  department')
      print
      for item in db_departments.values():
        print(item._idDept, ' | ', item.nameDept)
        print
    elif options == 'q':
      break

print(client_db)