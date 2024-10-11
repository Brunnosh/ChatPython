
from database.entities import User
from database.mongoHandler import MongoHandler, Operations


def enviarMenssagem():
    print("Digite a menssagem")
    mensagem = input(":")



if __name__ == '__main__':
    handler = MongoHandler()
    operation = Operations()


    email = input("Email:")
    senha = input("Senha:")

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
                    #Enviar mensagem
                    enviarMenssagem()



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




