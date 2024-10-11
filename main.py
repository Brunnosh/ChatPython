import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
from database.entities import User, Message
from database.mongoHandler import MongoHandler, Operations, add_new_user, is_there_user, update_password, delete_user


# Função para derivar a chave
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# Função para gerar um novo salt
def generate_salt() -> bytes:
    return os.urandom(16)  # 16 bytes de salt

if __name__ == '__main__':
    handler = MongoHandler()


    while True:
        print("[1] - Criar conta")
        print("[2] - Fazer login")
        print("[3] - Alterar senha")
        print("[4] - Deletar conta")
        print("[5] - Sair")

        escolha = input("escolha:")

        match escolha:

            case "1":
                emailinput = input("Email:")
                senhainput = input("Senha:")

                ret = add_new_user(emailinput,senhainput)
                if isinstance(ret, str):
                    print(ret)  # Mensagem de erro se o usuário já existir
                else:
                    print("Usuário registrado com sucesso!")

            case "2":
                email = input("Email:")
                senha = input("Senha:")


                if handler.auth(email, senha):
                    print("Usuário logado")

                    # Solicitar a senha para derivar a chave
                    password = input("Insira a senha para a criptografia: ")
                    salt = generate_salt()  # Gerar um salt
                    key = derive_key(password, salt)
                    fernet = Fernet(key)  # Inicializa Fernet com a chave derivada

                    operations = Operations(email, senha, salt)

                    while True:
                        print("[1] - Enviar mensagem")
                        print("[2] - Checar mensagens (Um contato)")
                        print("[3] - Listar contatos")
                        print("[4] - Trocar senha de criptografia")
                        print("[5] - Sair")

                        opcao = input("Opção: ")

                        match opcao:
                            case "1":
                                # Enviar mensagem
                                destino = input("Para: ")
                                conteudo = input("Mensagem: ")
                                # Criptografar a mensagem
                                conteudo_cripto = fernet.encrypt(conteudo.encode()).decode()
                                msg = Message(email, destino, conteudo_cripto)
                                operations.add_new_message(msg, salt)  # Armazena também o salt
                                print("Mensagem enviada com sucesso!")

                            case "2":
                                # Consultar mensagens de um contato específico
                                contato = input("Contato: ")
                                mensagens = operations.retrieve_messages_from_contact(email, contato)
                                if mensagens:
                                    for m in mensagens:
                                        try:
                                            # Decodificar o salt de volta para bytes
                                            salt = base64.b64decode(m['salt'].encode())
                                            # Derivar a chave com o salt armazenado
                                            key = derive_key(password, salt)  # Usar o salt da mensagem
                                            fernet = Fernet(key)
                                            # Descriptografar a mensagem
                                            conteudo_descripto = fernet.decrypt(m['content'].encode()).decode()
                                            print(f"{m['email_from']} -> {m['email_to']}: {conteudo_descripto}")
                                        except InvalidToken:
                                            print(f"Erro ao descriptografar mensagem de {m['email_from']}.")
                                        except Exception as e:
                                            print(f"Ocorreu um erro: {str(e)}")

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
                                # Trocar senha de criptografia
                                password = input("Insira a nova senha para a criptografia: ")
                                print("Senha de criptografia atualizada com sucesso.")

                            case "5":
                                print("Saindo...")
                                exit()

                            case _:
                                print("Opção inválida, tente novamente.")
                else:
                    if is_there_user(email):
                        print("Senha inválida")
                    else:
                        print("Usuário não encontrado")


            case "3":
                emailTrocaSenha = input("Email:")
                novaSenha = input("Nova senha:")
                update_password(emailTrocaSenha, novaSenha)

            case "4":
                emailDeletarConta = input("Email:")
                senhaDeletarConta = input("Senha:")
                delete_user(emailDeletarConta,senhaDeletarConta)



            case "5":
                break


