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

def update_user(username, new_aboutme):
    usercollection.update_one(
        {"username": username},
        {"$set": {"about me": new_aboutme}}
    )
    return True

def update_password(username, new_password):
    usercollection.update_one(
        {"username": username},
        {"$set": {"password": new_password}}
    )
    return True

def add_new_user(username, data):
    if check_username(username) != True:
      usercollection.insert_one(data)
      return True
    else:
      return False

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
  
def write_to_database_by_name(username, data):
  usercollection.update_one(
        {"username": username},
        #this is not gonna work data in data? nah it gonna replaced
        {"$set": {"data": data}}
    )
  return True
