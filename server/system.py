from encryption.encrypt import *
from authentication.auth import *
from user_managment import User

# Secret_key do servidor


# ---------------------Dados de usuários (simulado em memória) ----------------
#global users_database # não precisa definir como global por que ela nao ta dentro de nenhuma função
users_database = []

# ------------------------- Registro do usuário -------------------------------
def register_user():
    login = input("Digite seu usuário: ")
    phone_number = input("Digite seu número de celular: ")
    password = input("Digite sua senha: ")
    salt = generate_salt()
    password_scrypt = derive_key_scrypt(salt, password) # senha hasheada

    user = User(login, phone_number, password_scrypt, salt)

    def addUserToDB(userToAdd: User):
        users_database.append(userToAdd)
        print("Usuário cadastrado com sucesso!")

    if len(users_database) == 0:
        addUserToDB(user)
        return

    for user in users_database:
        if user.login == login:
            print("Usuário já cadastrado com esse login")
        elif user.phone == phone_number:
            print("Usuário já cadastrado com esse telefone")
        else:
            addUserToDB(user)
            print("Usuário cadastrado com sucesso!")

# ------------------------- Login ------------------------------------
def login():
    login = input("Digite seu login: ")
    password = input("Digite sua senha: ")

    for c in range(len(users_database)):
        person = users_database[c]
        if person.login == login:
            userToLogin = person

            # Hasheando a senha recebida com scrypt e comparando com a que tem guardada
            salt_received_password = userToLogin.salt # salt_received_password = generate_salt()   
            scrypt_received_password = derive_key_scrypt(salt_received_password, password)

            if userToLogin.password == scrypt_received_password:
                # Segundo fator de autenticação
                user_secret = generate_2fa_code(userToLogin.secret_key)
                server_secret = generate_2fa_code(userToLogin.secret_key)

                if user_secret == server_secret:
                    print(f"\nBem-vindo, {userToLogin.login}!")
                    #return # a partir daqui ele deve ir para o server_menu()
                else:
                    print("\nAutenticação falhou!")
            else:
                print("\nSenha incorreta.")

        else: #person == None and c == len(users_database)
            print("\nUsuário não encontrado.")

# ---------------------- Escolher o usuário --------------------------
def choose_user():
    print("Para enviar uma mensagem você precisa escolher um usuário")
    for user in users_database:
        print(f"{user.login}\n")

    login = input("Escreva o nome do usuário que deseja enviar uma mensagem: ")

    for user in users_database:
        if user.login == login:
            return user


'''
Percebi que a gente precisa de um menu geral e um menu para o servidor.
E o menu do servidor só pode ser acessado depois do login
'''
# ---------------------- Menu de entrada --------------------------

def entry_menu():
    print("\n1. Cadastro")
    print("2. Login")
    print("3. Sair")
    option = input("Escolha uma opção: ")
    return option

# ---------------------- Menu do servidor --------------------------
def server_menu():
    print("1. Enviar mensagem")
    print("2. Comando especial")
    print("3. Sair")
    option = input("Escolha uma opção: ")
    return option

# ---------------------- Mostrar dados dos usuários --------------------------
def showUsersData():
    for user in users_database:
        print("\nlogin: " + user.login)
        print("phone: " + user.phone)
        print("password: " + str(user.password))
        print("salt: " + str(user.salt))
        print("secret_key: " + user.secret_key)

    back = input("\nDigite 0 (zero) para voltar: ")
    if back == 0:
        server_menu()


# Menu principal
while True:
    option = entry_menu()
    if option == "1":
        register_user()
    elif option == "2":
        login()
    elif option == "3":
        break
    else:
        print("Opção inválida. Tente novamente.")


'''
if server == True:
            option = server_menu()
            if option == "1":
                choose_user()
            elif option == "2":
                showUsersData()
            elif option == "3":
                entry_menu()
            else:
                print("Opção inválida. Tente novamente.")
'''

