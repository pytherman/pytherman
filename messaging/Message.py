from enum import Enum


MessageType = Enum('MessageType', 'INTENT COLLISION DAMAGE')


class Message(object):
    def __init__(self, type):
        self.type = type


Intent = Enum('Intent', 'MOVE_UP MOVE_DOWN MOVE_RIGHT MOVE_LEFT \
                         MOVE_CLEAR_VERTICAL MOVE_CLEAR_HORIZONTAL')


class IntentMessage(Message):
    def __init__(self, intent):
        super().__init__(MessageType.INTENT)
        self.intent = intent
