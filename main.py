
from database.entities import User
from database.mongoHandler import MongoHandler, Operations
from database.entities import Message
def menviaMensagem():
    nickname_from = email
    nickname_to = input("Digite para quem deseja enviar: ")
    content = input("Digite A mensagem ")
    m = Message(nickname_from,nickname_to,content)
    operation.add_new_message(m)



if __name__ == '__main__':
    handler = MongoHandler()

    email = input("Email:")
    senha = input("Senha:")

    operation = Operations(email,senha)



    if handler.auth(email, senha):
        print("usuario logado")

        repete = 0
        while repete == 0:
            repete = 0

            print("[1] - Enviar mensagem")
            print("[2] - Checar mensagens (Todas)")
            print("[3] - Checar mensagens (Um contato)")
            print("[4] - Sair")

            repete = input("Opção:")

            match repete:
                case "1":
                    menviaMensagem()
                    #Enviar mensagem
                case 2:
                    exit()
                    # Consultar todas mensagens
                case 3:
                    exit()
                    # Consultar mensagem de um contato
                case 4:
                    repete = 0





    else:
        print("Usuário não encontrado")


