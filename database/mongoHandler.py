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
    def __init__(self, email: str, password: str):

        self.connection_string = connectionstring
    def add_new_message(self, m: Message):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages
        return coll.insert_one(m.__dict__).inserted_id

    def retrieve_message(self, email : str):

        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages
        messages = coll.find({
            "$or": [
                {"nickname_from": email},
                {"nickname_to": email}
            ]
        })

        return list(messages)

    def retrieve_messages_from_contact(self, email: str, contact: str):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages

        # Recuperar mensagens entre o usuário e um contato específico
        messages = coll.find({
            "$or": [
                {"nickname_from": email, "nickname_to": contact},
                {"nickname_from": contact, "nickname_to": email}
            ]
        })

        return list(messages)