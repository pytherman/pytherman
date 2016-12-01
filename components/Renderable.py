class Renderable:
    def __init__(self, image):
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()
        print(self.w, " ", self.h)
