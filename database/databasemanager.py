
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['Database1']
usercollection = db['db1']


def access_database(username):
  usertarget_data = usercollection.find_one({"username": username})
  return usertarget_data

def delete_user(username):
  usercollection.delete_one({"username": username})
  return True

def update_user(username, data):
  usercollection.update_one({"username": username}, {"$set": data})
  return True

def add_new_user(username, data):
  if check_username!= True:
    usercollection.insert_one(data)
  return True

def check_username(username):
  user_from_db = access_database(username)
  if user_from_db != None or user_from_db != '':
    return True
  else:
    return False

def check_database_status():
  try:
    # Try to connect to the MongoDB server
    client = MongoClient(client)
    client.server_info()
    return True
  except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    return False
  
