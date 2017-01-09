from enum import Enum


MessageType = Enum('MessageType', 'Command Collision Damage')


class Message(object):
    def __init__(self, type):
        self.type = type
