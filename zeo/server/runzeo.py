from ZEO.ClientStorage import ClientStorage
from ZODB import DB
import transaction, ZODB.tests.util
from ZODB.PersistentMapping import PersistentMapping
from Persistence import Persistent
import shortuuid
import ZEO

CONSTANTS_DEPARTMENT = 'DEPARTMENTS'
LIST_DEPARTMENT = ['Accounting', 'Audit', 'Sales', 'Administration', 'Human Resources', 'Financial']

# initial server
print("###########starting ZEO Server###########")
# storage=ClientStorage(('localhost',8090))
# print("storage opened")
# db=DB(storage)
# conn=db.open()
# print("connection opened")
# root=conn.root()
# print("established connection")

connection = ZEO.connection(('localhost',8090))
root = connection.root()

# end initial connection
class Department(Persistent):
  def __init__(self, _idDept, nameDept):
    self._idDept = _idDept
    self.nameDept = nameDept

def initialDepartment(collection):
  for department in LIST_DEPARTMENT:
    unique_id = str(shortuuid.uuid())
    try:
      print(unique_id, department)
      print('=>>>', unique_id, ' - ', department)
      collection[unique_id]=Department(unique_id, department)
    except KeyError:
      print('initial department error!')
      return
      print
  root[CONSTANTS_DEPARTMENT] = collection
  transaction.commit()
  print('###Initial Department successfull!###')
  print

if CONSTANTS_DEPARTMENT not in root.keys():
  root[CONSTANTS_DEPARTMENT] = {}
  db_department = root[CONSTANTS_DEPARTMENT]
  initialDepartment(db_department)

# list department
def _getListDepartment():
  if len(root[CONSTANTS_DEPARTMENT].values()) == 0:
    print('There are no departments.', root)
    print
    return
  print('#######LIST DEPARTMENT#######')
  print('______________________id|  department')
  print
  for item in root[CONSTANTS_DEPARTMENT].values():
    print(item._idDept, ' | ', item.nameDept)
    print

# main program
if __name__ == '__main__':
  while 1:
    print('#########MENU###########')
    print('# L. LIST DEPARTMENT   #')
    print('# Q. QUIT PROGRAM     #')
    print('########################')
    options = input('Select a option: ')
    options = options.lower()
    if options == 'l':
      _getListDepartment()
    elif options == 'q':
      break

print("closed")
