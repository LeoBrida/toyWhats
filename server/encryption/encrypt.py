from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
import os

# Função para criar um salt aleatório
def generate_salt():
    return os.urandom(16)

# Função para derivar uma chave a partir da senha e do salt usando SCRYPT
def derive_key_scrypt(salt, password):
    return scrypt(password, salt, 32, N=2**14, r=8, p=1) # Revisar parâmetros para serem escolhidos

def derive_key_pbkdf2(salt, password):
    return PBKDF2(password, salt, 16, 1000, None, SHA512) # Revisar parâmetros para serem escolhidos

# Função para criar um par de chaves AES (chave de criptografia e IV) a partir da senha e do salt
def generate_aes_keys(salt, password):
    key = derive_key_pbkdf2(salt, password)
    iv = os.urandom(16)
    return key, iv

# Função para cifrar uma mensagem usando AES-GCM
def encrypt_message(message, key, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
    return ciphertext, tag #cipher.nonce

# Função para decifrar uma mensagem usando AES-GCM
def decrypt_message(ciphertext, key, iv, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode('utf-8')
