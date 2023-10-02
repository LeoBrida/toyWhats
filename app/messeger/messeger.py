from objects.object_user import  User, Message
from encryption.encrypt import *

def sendMessageToUser(selectedUser: User, loggedUser: User):
        text = input('Mensagem: ')
       
        messageSended = Message(text, loggedUser.login, selectedUser.login)
        loggedUser.addSendedMessage(messageSended)

        messageP = derive_key_scrypt(selectedUser.salt, text)
        key = generate_aes_keys(selectedUser.salt, messageP)

        iv = generate_aes_ivs(loggedUser.salt)
        ciphertext, tag, nonce = encrypt_message(text, key, iv)

        messageToSend = Message(ciphertext, loggedUser.login, selectedUser.login, tag, nonce, messageP)
        selectedUser.addReceivedMessage(messageToSend)
        

        print("\nMensagem enviada!\n")

def readSendedMessages(selectedUser: User):
        if len(selectedUser.sended_messages) == 0:
                print("\nVocê não enviou nenhuma mensagem ainda :(\n")
        else:
                print('\n')
                for message in selectedUser.sended_messages:
                        print(f"Para {message.receiver}:")
                        print('"' + message.text + '"\n')
                print("")

def readReceivedMessages(loggedUser: User): #receiver: User
        if len(loggedUser.received_messages) == 0:
                print("\nNenhuma mensagem recebida :(\n")

        else:
                print('\n')
                for index, message in enumerate(loggedUser.received_messages):
                        print(f"De {message.sender}:")
                        print('"' + str(message.text) + '"')
                        print(f"Index: {index}\n")
                print("")

        askDecryptMessage = None

        if len(loggedUser.received_messages) != 0:
                askDecryptMessage = input('\nDeseja descriptografar alguma mensagem [S | N]:').upper()

        if askDecryptMessage == "S":
                messageIndex = int(input('Digite o index da mensagem que deseja descriptografar: '))
                messageToDecrypt = loggedUser.received_messages[messageIndex]
                decryptedMessage = decryptReceivedMessage(messageToDecrypt, loggedUser)
                
                print('\n')
                print(f"Mensagem descriptografada de {messageToDecrypt.sender}:")
                print('"' + str(decryptedMessage) + '"')
                print('\n')

def decryptReceivedMessage(message: Message, user: User): #aqui não rola de ser user pq ele ta usando a o loggeduser e o loggedUser que le a mensagem não foi o mesmo que enviou
        key = generate_aes_keys(user.salt, message.messageP) 
        iv = message.nonce

        return decrypt_message(message.text, key, iv, message.tag)
