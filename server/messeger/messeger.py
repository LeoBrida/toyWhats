from objects.object_user import  User, Message
from encryption.encrypt import *

def sendMessageToUser(selectedUser: User, loggedUser: User):
        text = input('Mensagem: ')
        key, iv = generate_aes_keys(loggedUser.salt, loggedUser.password)
       
        messageSended = Message(text, loggedUser.login, selectedUser.login)
        loggedUser.addSendedMessage(messageSended)

        ciphertext, tag, nonce = encrypt_message(text, key, iv)
        messageToSend = Message(ciphertext, loggedUser.login,selectedUser.login, tag)
        selectedUser.addReceivedMessage(messageToSend)
        

        print("\nMensagem enviada\n")

def readSendedMessages(selectedUser: User):
        if len(selectedUser.sended_messages) == 0:
                print("\nNenhuma mensagem enviada\n")
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
                for message in selectedUser.received_messages:
                        print("\n")
                        print(f"De {message.sender}:")
                        print('"' + str(message.text) + '"')
                        print("\n")

def decryptReceivedMessage(message: Message, iv, user: User):
        key, iv = generate_aes_keys(user.salt, user.password)
        return decrypt_message(message.text, key, iv, message.tag)
        