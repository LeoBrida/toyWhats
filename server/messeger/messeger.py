from objects.object_user import  User, Message
from encryption.encrypt import *

def sendMessageToUser(selectedUser: User, loggedUser: User):
        text = input('Mensagem: ')
        # msg = encrypt_message(text, None, None) # tem que gerar key e iv
        # messageToSend = Message(msg.ciphertext, loggedUser.login, selectedUser)
        messageToSend = Message(text, loggedUser.login, selectedUser.login)
        
        selectedUser.addReceivedMessage(messageToSend)
        loggedUser.addSendedMessage(messageToSend)

        print("\nMensagem enviada\n")

def readSendedMessages(selectedUser: User):
        if len(selectedUser.sended_messages) == 0:
                print("\nNenhuma mensagem recebida\n")
        else:
                for message in selectedUser.sended_messages:
                        print("\n")
                        print(f"Para {message.receiver}:")
                        print('"' + message.text + '"')
                        print("\n")

def readReceivedMessages(selectedUser: User):
        if len(selectedUser.received_messages) == 0:
                print("\nNenhuma mensagem recebida\n")
        else:
                for message in selectedUser.sended_messages:
                        print("\n")
                        print(f"De {message.sender}:")
                        print('"' + message.text + '"')
                        print("\n")
