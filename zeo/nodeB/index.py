# from ZODB import FileStorage, DB
import ZODB.config

# storage = FileStorage.FileStorage('test-filestorage.fs')
# db = DB(storage)
db = ZODB.config.databaseFromURL('test.conf')
conn = db.open()