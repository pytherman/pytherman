class Renderable:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()
        print(self.w, " ", self.h)
