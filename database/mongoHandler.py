from operator import truediv
from pymongo import MongoClient

from database.entities import Message

from pymongo import MongoClient

from database.mongoconnection import connectionstring


class MongoHandler:
    def __init__(self):
        self.client = MongoClient(connectionstring)

    def connect(self, db_name):

        return self.client[db_name]

    def auth(self, email, password) -> bool:
        db = self.connect("chat")
        user = db.users.find_one({"email":email, "password": password})
        if user:
            return True
        else:
            return False

class Operations:
    def __init__(self, username: str, password: str, primary_node:str):

        self.connection_string = \
            ('mongo+srv://{}:{}@{}?retryWrites=true'.format(username, password, primary_node))

    def add_new_message(self, m: Message):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages
        return coll.insert_one(m.__dict__).inserted_id