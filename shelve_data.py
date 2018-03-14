import shelve
from config import shelve_name
db = shelve.open(shelve_name)
print (db.keys(), db.values())
db.items()
db.close()