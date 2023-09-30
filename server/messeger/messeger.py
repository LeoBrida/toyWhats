from objects.object_user import  User
from objects.object_message import Message
from encryption.encrypt import *


def sendMessageToUser(selectedUser: User):
        text = input('Mensagem: ')
        msg = encrypt_message(text, None, None) # tem que gerar key e iv
        messageToSend = Message(msg.ciphertext, loggedUser.login, selectedUser)
        
        selectedUser.addReceivedMessage(messageToSend)
        loggedUser.addSendedMessage(messageToSend)

        print("Mensagem enviada")