from authentication.auth import *
from encryption.encrypt import *

class User():
    def __init__(self, login, phone, password, salt):
        self.login = login
        self.phone = phone
        self.password = password
        self.salt = salt
        self.secret_key = generate_2fa_secret()

    def send_message():
        pass

    def receive_message():
        pass