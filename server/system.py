from encryption.encrypt import *
from authentication.auth import *
from objects.object_user import User
from objects.object_message import Message

# --------------------- Secret_key do servidor --------------------------------


# --------------------- Dados de usuários (simulado em memória) ----------------
users_database = []

def setLoggedUser(user):
    loggedUser = user

# ------------------------- Registro do usuário -------------------------------
def register_user():
    login = input("Digite seu usuário: ")
    phone_number = input("Digite seu número de celular: ")
    password = input("Digite sua senha: ")
    salt = generate_salt()
    password_scrypt = derive_key_scrypt(salt, password) # senha hasheada

    userToAdd = User(login, phone_number, password_scrypt, salt)

    hasEqualPhone = any(user.phone == phone_number for user in users_database)
    hasEqualLogin = any(user.login == login for user in users_database)

    def addUserToDB(userToAdd: User):
        users_database.append(userToAdd)
        print("Usuário cadastrado com sucesso!")

    if len(users_database) == 0:
        addUserToDB(userToAdd)
    elif hasEqualPhone:
        print("Usuário já cadastrado com esse telefone")
    elif hasEqualLogin:
        print("Usuário já cadastrado com esse login")
    else:
        addUserToDB(userToAdd)

# ------------------------- Login ------------------------------------
def login():
    login = input("Digite seu login: ")
    password = input("Digite sua senha: ")

    for c in range(len(users_database)):
        user = users_database[c]
        if user.login == login:
            userToLogin = user

            # Hasheando a senha recebida com scrypt e comparando com a que tem guardada
            salt_received_password = userToLogin.salt
            scrypt_received_password = derive_key_scrypt(salt_received_password, password)

            if userToLogin.password == scrypt_received_password:
                # Segundo fator de autenticação
                user_secret = generate_2fa_code(userToLogin.secret_key)
                server_secret = generate_2fa_code(userToLogin.secret_key)

                if user_secret == server_secret:
                    global loggedUser
                    loggedUser = userToLogin
                    print(f"\nBem-vindo, {loggedUser.login}!")
                else:
                    print("\nAutenticação falhou!")
            else:
                print("\nSenha incorreta.")

        else: #person == None and c == len(users_database)
            print("\nUsuário não encontrado.")

# ---------------------- Escolher o usuário --------------------------
def sendMessage():
    print("Para enviar uma mensagem você precisa escolher um usuário\n")
    for user in users_database:
        print(f"{user.login}")

    selectedUsername = input("Escreva o nome do usuário que deseja enviar uma mensagem: ")
    userFoundedOnDB = next((user for user in users_database if user.login == selectedUsername), None)


    if userFoundedOnDB:
        print(f'Usuário "{userFoundedOnDB.login}" encontrado\n')
        sendMessageToUser(userFoundedOnDB)
    else:
        print(f'Usuário "{selectedUsername}" não encontrado!')

# ---------------------- Enviar mensagem ----------------------------
def sendMessageToUser(selectedUser: User):
        text = input('Mensagem: ')
        ciphertext, tag = encrypt_message(text, None, None) # tem que gerar key e iv para colocar aqui
        messageToSend = Message(ciphertext, loggedUser.login, selectedUser, tag)
        
        selectedUser.addReceivedMessage(messageToSend)
        loggedUser.addSendedMessage(messageToSend)

        print("Mensagem enviada")

# ---------------------- Receber mensagem ----------------------------
def receiveMessageFromUser():
    pass
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

def chooseOption():
    if loggedUser:
        option = server_menu()

        if option == "1":
            sendMessage()
        elif option == "2":
            showUsersData()
        elif option == "3":
            return "exit"
        else:
            print("Opção inválida. Tente novamente.")
    else:
        option = entry_menu()

        if option == "1":
            register_user()
        elif option == "2":
            login()
        elif option == "3":
            return "exit"
        else:
            print("Opção inválida. Tente novamente.")

# Menu principal
while True:
    option = chooseOption()
    if option == "exit":
        break
