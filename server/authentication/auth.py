import os
import base64
from pyotp import TOTP

# Função para gerar uma chave secreta de autenticação de dois fatores
def generate_2fa_secret():
    return base64.b32encode(os.urandom(20)).decode("utf-8")

# Função para gerar um código TOTP de autenticação de dois fatores
def generate_2fa_code(secret):
    totp = TOTP(secret)
    return totp.now()