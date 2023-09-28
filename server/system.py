from encryption.encrypt import *
from authentication.auth import *
from user_managment import User


# Dicionário para armazenar os dados de usuário (simulado em memória)
users_database = []

def register_user():
    login = input("Digite seu usuário: ")
    phone_number = input("Digite seu número de celular: ")
    password = input("Digite sua senha: ")
    salt = generate_salt()
    password_scrypt = derive_key_scrypt(salt, password)

    user = User(login, phone_number, password_scrypt, salt)

    for user in users_database:
        if user.login == login:
            print("Usuário já cadastrado com esse login")
        elif user.phone_number == phone_number:
            print("Usuário já cadastrado com esse telefone")
        else:
            users_database.append(user)
            print("Usuário cadastrado com sucesso!")


def login():
    login = input("Digite seu login: ")
    password = input("Digite sua senha: ")

    for u in users_database:
        if u.login == login:
            user = u
        if pbkdf2_sha256.verify(password, usuario["senha_hash"]): # essa é uma função de uma outra lib, eu acho que temos que bater a senha com o scrypt
            secret = generate_2fa_code(user.secret_key)
            print(f"Bem-vindo, {usuario['nome']}!")
        else:
            print("Senha incorreta.")
    else:
        print("Usuário não encontrado.")

def list_users_data():
    print("Login\t")
    print("Celular\t")
    print("Scrypt Senha\t")
    print("Salt\n")

    for user in users_database:
        print(f"{user.login}\t")
        print(f"{user.phone}\t")
        print(f"{user.password}\t")
        print(f"{user.salt}\n")

    voltar = input("Digite 0 (zero) para voltar")
    if voltar == 0:
        menu()

def choose_user():
    print("Para enviar uma mensagem você precisa escolher um usuário")
    for person in users_database:
        print(f"{person.login}\n")
    login = input("Escreva o nome do usuário para enviar uma mensagem:")

    for user in users_database:
        return user #corrigir


# Menu principal
while True:
    def menu():
        print("\n1. Cadastro")
        print("2. Login")
        print("3. Enviar mensagem")
        print("4. Sair")
        option = input("Escolha uma opção: ")

        if option == "1":
            register_user()
        elif option == "2":
            login()
        elif option == "3":
            choose_user()
        elif option == "3":
            break
        else:
            print("Opção inválida. Tente novamente.")






