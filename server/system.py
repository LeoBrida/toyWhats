from encryption.encrypt import *
from authentication.auth import *
from user_managment import User


def register():
    # um usuário novo deve se cadastrar com login, número do celular, e senha de acesso.
    # Registro do usuário
    salt = generate_salt()
    key, iv = generate_aes_keys(salt, password)
    user_data = { # puxar dos dados
        "username": username,
        "phone_number": phone_number,
        "password_salt": salt,
        "encryption_key": key,
        "encryption_iv": iv
    }
    pass

def user_login():
    # Sempre que o usuario entrar no sistema ele deve ser autenticado
    #É preciso autenticar usuários usando login/senha e um segundo fator de autenticação (cada usuário deve ter um “secret key” diferente cadastrado para obter o segundo fator);
    pass

def users_list():
    pass


# Exemplo de uso:

# Dados do usuário (simulação)
username = "nome1"
phone_number = "999223344"
password = "senha1"

# Mensagem a ser enviada
message_to_send = "Olá, usuário2!"

# Simulação do envio da mensagem
# Suponha que o destinatário seja "nome2" e você tenha acesso aos dados do usuário destinatário

# Cifrar a mensagem
ciphertext, nonce, tag = encrypt_message(message_to_send, user_data["encryption_key"], user_data["encryption_iv"])

# Armazenar a mensagem cifrada e outros dados relevantes (como nonce e tag) para entrega ao destinatário

# Simulação da recepção da mensagem pelo destinatário
# Suponha que o destinatário seja "nome2" e você tenha acesso aos dados do usuário destinatário

# Decifrar a mensagem
plaintext = decrypt_message(ciphertext, user_data["encryption_key"], nonce, tag)

# Exibir a mensagem decifrada
print(f"Mensagem recebida: {plaintext}")