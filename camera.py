
from vector import Vector2


class Camera(object):
    def __init__(self, width, height, center_pos=Vector2(0, 0)):
        self.width, self.height = width, height
        self.pos = center_pos - Vector2(width // 2, height // 2)

    def world_to_screen(self, world_pos):
        return world_pos - self.pos

    def screen_to_world(self, screen_pos):
        return screen_pos + self.pos

    def move(self, vel):
        self.pos += vel
