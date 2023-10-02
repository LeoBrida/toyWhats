from objects.object_user import  User, Message
from encryption.encrypt import *

def sendMessageToUser(selectedUser: User, loggedUser: User):
        text = input('Mensagem: ')
       
        messageSended = Message(text, loggedUser.login, selectedUser.login)
        loggedUser.addSendedMessage(messageSended)

        key, iv = generate_aes_keys(loggedUser.salt, loggedUser.password)
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

def readReceivedMessages(loggedUser: User, receiver: User):
        if len(loggedUser.received_messages) == 0:
                print("\nNenhuma mensagem recebida\n")

        else:
                for index, message in enumerate(loggedUser.received_messages):
                        print("\n")
                        print(f"De {message.sender}:")
                        print('"' + str(message.text) + '"')
                        if message.text is not str:
                                print(f"\nIndex da mensagem: {index}")
                        print("\n")

        askDecryptMessage = None

        if len(loggedUser.received_messages) != 0:
                askDecryptMessage = input('\nDeseja descriptografar alguma mensagem [S | N]:').upper()

        if askDecryptMessage == "S":
                messageIndex = input('\nDigite o index da mensagem que deseja descriptografar: ')
                messageToDecrypt = loggedUser.received_messages[int(messageIndex)]
                decryptedMessage = decryptReceivedMessage(messageToDecrypt, loggedUser)
                
                print(f"De {messageToDecrypt.sender}:")
                print('"' + str(decryptedMessage) + '"')

def decryptReceivedMessage(message: Message, user: User):
        key, iv = generate_aes_keys(user.salt, user.password)
        return decrypt_message(message.text, key, iv, message.tag)
