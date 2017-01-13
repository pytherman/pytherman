"""Physics component"""


class Physics(object):
    """Physics component allows to simulate physics for entity."""

    def __init__(self, body, user_data=None):
        self.body = body
