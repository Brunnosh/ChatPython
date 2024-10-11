
from database.entities import User, Message
from database.mongoHandler import MongoHandler, Operations

if __name__ == '__main__':
    handler = MongoHandler()

    email = input("Email:")
    senha = input("Senha:")

    if handler.auth(email, senha):
        print("usuario logado")

        repete = 0

        operations = Operations(email,senha)
        while True:
            print("[1] - Enviar mensagem")
            print("[2] - Checar mensagens (Um contato)")
            print("[3] - Listar contatos")
            print("[4] - Trocar chave de criptografia")
            print("[5] - Sair")

            opcao = input("Opção: ")

            match opcao:
                case "1":
                    # Enviar mensagem
                    destino = input("Para: ")
                    conteudo = input("Mensagem: ")
                    msg = Message(email, destino, conteudo)
                    operations.add_new_message(msg)
                    print("Mensagem enviada com sucesso!")

                case "2":
                    # Consultar mensagens de um contato específico
                    contato = input("Contato: ")
                    mensagens = operations.retrieve_messages_from_contact(email, contato)
                    if mensagens:
                        for m in mensagens:
                            print(f"{m['email_from']} -> {m['email_to']}: {m['content']}")
                    else:
                        print(f"Nenhuma mensagem com {contato} encontrada.")

                case "3":
                    # Listar todos os contatos com os quais já trocou mensagens
                    contatos = operations.list_all_contacts(email)
                    if contatos:
                        print("Contatos com os quais você já trocou mensagens:")
                        for contato in contatos:
                            print(contato)
                    else:
                        print("Você ainda não trocou mensagens com ninguém.")

                case "4":
                    print("Saindo...")
                    break

                case "5":
                    print("Saindo...")
                    break

                case _:
                    print("Opção inválida, tente novamente.")




    else:
        print("Usuário não encontrado")


