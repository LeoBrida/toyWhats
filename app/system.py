from encryption.encrypt import *
from authentication.auth import *
from objects.object_user import User, Message
from messeger.messeger import *
import json


# --------------------- Dados de usuários (simulado em memória) ----------------
users_database = []
users_persistence = []
loggedUser = None

def setLoggedUser(user: User):
    global loggedUser
    loggedUser = user

# ------------------------- Registro do usuário -------------------------------
def register_user():
    login = input("\nDigite seu usuário: ")
    phone_number = input("Digite seu número de celular: ")
    password = input("Digite sua senha: ")
    salt = generate_salt()
    password_scrypt = derive_key_scrypt(salt, password) # senha hasheada
    global salt_user
    salt_user = salt

    user = {'Login': login, 'Phone': phone_number, 'PasswordScript': str(password_scrypt), 'Salt': str(salt)}
    users_persistence.append(user)
    file = 'usersDataFile.json'
    loadOnFile = open(file, 'w')
    json.dump(users_persistence, loadOnFile)
    loadOnFile.close()

    userToAdd = User(login, phone_number, password_scrypt, salt)

    hasEqualPhone = any(user.phone == phone_number for user in users_database)
    hasEqualLogin = any(user.login == login for user in users_database)

    def addUserToDB(userToAdd: User):
        users_database.append(userToAdd)
        print("\nUsuário cadastrado com sucesso!")

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
    login = input("\nDigite seu login: ")
    password = input("Digite sua senha: ")

    #userFoundedOnDB = next((user for user in users_database if user.login == login), None)
    usersReg = open('usersDataFile.json', 'r')
    data = json.load(usersReg)
    userRegistered = next((user for user in data if user["Login"] == login), None)
    usersReg.close()

    '''if userFoundedOnDB == None:
        print("\nUsuário não encontrado.")'''
    if userRegistered == None:
        print("\nUsuário não encontrado.")
    else:
        # Hasheando a senha recebida com scrypt e comparando com a que tem guardada
        scrypt_received_password = derive_key_scrypt(userRegistered["Salt"], password)

        print(userRegistered["Salt"])
        #print(salt_user)

        print(scrypt_received_password)
        print(userRegistered["PasswordScript"] )

        if userRegistered["PasswordScript"] == str(scrypt_received_password):
            # Segundo fator de autenticação
            totp, current_code = generate_2fa_code(userFoundedOnDB.secret_key)
            print(f"\n  Digite o código TOTP para realizar a autenticação: {current_code}\n")
            entered_code = input("Código TOTP: ")

            if totp.verify(entered_code):
                global loggedUser
                setLoggedUser(userFoundedOnDB)
                print(f"\nBem-vindo, {loggedUser.login}!\n")
            else:
                print("\nAutenticação falhou!")
        else:
            print("\nSenha incorreta.")

# ---------------------- Escolher o usuário --------------------------
def sendMessage():
    print("Para enviar uma mensagem você precisa escolher um usuário\n")
    for user in users_database:
        print(f"{user.login}")

    selectedUsername = input("\nEscreva o nome do usuário que deseja enviar uma mensagem: ")
    userFoundedOnDB = next((user for user in users_database if user.login == selectedUsername), None)

    if userFoundedOnDB:
        print(f'Usuário "{userFoundedOnDB.login}" encontrado\n')
        sendMessageToUser(userFoundedOnDB, loggedUser)
    else:
        print(f'Usuário "{selectedUsername}" não encontrado!')

# ---------------------- Receber mensagem ----------------------------
def receiveMessageFromUser():
    #mostrar mensagens
    i = 0
    dic = {}
    for msg in loggedUser.received_messages:
        i += 1
        dic[i] = msg
        print(f"{i}. {msg}")
    
    selectedMessage = input("Selecione o numero da mensagem que quer ler: ")
    messageToRead = dic[selectedMessage]

    #não sei se gera a chave e o iv aqui desse user

    messageDecrypted = decrypt_message(messageToRead.ciphertext, None, None, messageToRead.tag) # tem que inserir chave  e iv nos Nones

    return print(f"Mensagem desencriptada: {messageDecrypted}")

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
    print("2. Ler mensagens recebidas")
    print("3. Ler mensagens enviadas")
    print("4. Logout")
    print("5. Sair")
    print("6. Mostrar dados dos usuários")

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
        print("received messages: " + str(len(user.received_messages)))
        print("\n")


def chooseOption():
    if loggedUser:
        option = server_menu()

        if option == "1":
            sendMessage()
        elif option == "2":
            readReceivedMessages(loggedUser)
        elif option == "3":
            readSendedMessages(loggedUser)
        elif option == "4":
            setLoggedUser(None)
        elif option == "5":
            return "exit"
        elif option == "6":
            showUsersData()
        else:
            print("\nOpção inválida. Tente novamente.")
    else:
        option = entry_menu()

        if option == "1":
            register_user()
        elif option == "2":
            login()
        elif option == "3":
            return "exit"
        else:
            print("\nOpção inválida. Tente novamente.")

# Menu principal
while True:
    option = chooseOption()
    if option == "exit":
        break
