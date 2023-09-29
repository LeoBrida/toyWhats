from encryption.encrypt import *
from authentication.auth import *
from user_managment import User

# Secret_key do servidor


# ---------------------Dados de usuários (simulado em memória) ----------------
global users_database
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

    global userToLogin #Não pode ser global, tem que ser local do método
    userToLogin = User

    for c in range(len(users_database)):
        person = users_database[c]

        if person.login == login:
            userToLogin = person
        elif userToLogin == None and c == len(users_database):
            print("Usuário não encontrado.")

    # Hasheando a senha recebida com scrypt e comparando com a que tem guardada
    # salt_received_password = generate_salt()      essa variável era assim. Mudei pq só assim as senhas batem. O salt precisa ser diferente nesse caso?
    salt_received_password = userToLogin.salt
    scrypt_received_password = derive_key_scrypt(salt_received_password, password)
    if userToLogin.password == scrypt_received_password:
        # Segundo fator de autenticação, usar o TOTP
        #secret_key -> getotp -> retorna numero (user e servidor)
        #comparar numero gerado pelo usuario e pelo servidor, se for o mesmo, ta autenticado
        user_secret = generate_2fa_code(userToLogin.secret_key)
        server_secret = generate_2fa_code(userToLogin.secret_key)
        
        if user_secret == server_secret:
            print(f"Bem-vindo, {userToLogin.login}!")
        else:
            print("Autenticação falhou!")
    else:
        print("Senha incorreta.")

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

# ---------------------- Escolher o usuário --------------------------
def choose_user():
    print("Para enviar uma mensagem você precisa escolher um usuário")
    for person in users_database:
        print(f"{person.login}\n")

    login = input("Escreva o nome do usuário que deseja enviar uma mensagem:")

    for user in users_database:
        if user.login == login:
            return user

def menu():
    print("\n1. Cadastro")
    print("2. Login")
    print("3. Enviar mensagem")
    print("4. Sair")
    print("5. Listar usuários")
    print("6. Comando especial")
    option = input("Escolha uma opção: ")

    return option

def showUsersData():
    for user in users_database:
        print("\n" + "login: " + user.login)
        print("phone: " + user.phone)
        print("password: " + str(user.password))
        print("salt: " + str(user.salt))
        print("secret_key: " + user.secret_key)

# Menu principal
while True:
    option = menu()

    if option == "1":
        register_user()
    elif option == "2":
        login()
    elif option == "3":
        choose_user()
    elif option == "4":
        break
    elif option == "5":
        list_users_data()
    elif option == "6":
        showUsersData()
    else:
        print("Opção inválida. Tente novamente.")





