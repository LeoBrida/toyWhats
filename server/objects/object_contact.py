from object_message import Message

class Contact:
    def __init__(self, username):
        self.username = username
        self.messages = []
      
    def addMessages(self, message: Message):
        self.messages.append(message)
