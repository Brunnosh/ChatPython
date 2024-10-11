import base64

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
    def __init__(self, email: str, password: str, salt : bytes):

        self.connection_string = connectionstring

    def add_new_message(self, m: Message, salt: bytes):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages
        m.__dict__['salt'] = base64.b64encode(salt).decode()  # Armazenar o salt
        return coll.insert_one(m.__dict__).inserted_id


    def retrieve_messages_from_contact(self, email: str, contact: str):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages

        # Recuperar mensagens entre o usuário e um contato específico
        messages = coll.find({
            "$or": [
                {"email_from": email, "email_to": contact},
                {"email_from": contact, "email_to": email}
            ]
        })

        return list(messages)

    def list_all_contacts(self, email: str):
        cli = MongoClient(self.connection_string)
        db = cli["chat"]
        coll = db.messages

        # Buscar todos os contatos que o usuário já trocou mensagens
        messages = coll.find({
            "$or": [
                {"email_from": email},
                {"email_to": email}
            ]
        })

        # Criar um conjunto único de contatos
        contacts = set()
        for msg in messages:
            if msg["email_from"] != email:
                contacts.add(msg["email_from"])
            if msg["email_to"] != email:
                contacts.add(msg["email_to"])

        return list(contacts)