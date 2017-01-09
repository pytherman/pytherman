class MessageBus(object):
    def __init__(self):
        self.messages = []

    def add(self, message):
        self.messages.append(message)

    def getByType(self, msg_type):
        return [msg for msg in self.messages if msg.type == msg_type]

    def clear(self):
        self.messages = []
