from operator import truediv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

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
            registerUser = input(
                f"Usuário não encontrado. Deseja criar uma conta com o email '{email}'? (s/n): ").lower()

            if registerUser == 's':
                # Chama a função para criar uma nova conta
                self.addUser(email, password)
                return True
            else:
                print("Encerrando o programa.")
                exit()

    def addUser(self, email, password):
        db = self.connect("chat")
        novo_usuario = {
            "email": email,
            "password": password
        }
        result = db.users.insert_one(novo_usuario)
        if result.inserted_id:
            print(f"Conta criada com sucesso para o email '{email}'!")
        else:
            print("Erro ao criar a conta.")


class Operations:
    def __init__(self, email: str, password: str):

        self.connection_string = connectionstring
    def add_new_message(self, m: Message):
        try:
            cli = MongoClient(self.connection_string)
            db = cli["chat"]
            coll = db.messages
            result = coll.insert_one(m.__dict__)
            return result.inserted_id
        except PyMongoError as e:
            print(f"Ocorreu um erro ao tentar enviar a mensagem: {e}")
            return None

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