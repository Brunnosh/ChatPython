
from database.entities import User
from database.mongoHandler import MongoHandler

if __name__ == '__main__':
    handler = MongoHandler()

    exists = handler.auth("brunotsavoia@gmail.com", "123")


    print(exists)