
import pygame
from game_object import GameObject
from vector import Vector2


class Paddle(GameObject):

    width = 100
    height = 20
    max_speed = 200

    @staticmethod
    def clamp_speed(vx):
        return max(-Paddle.max_speed, min(Paddle.max_speed, vx))

    def __init__(self, camera, pos, normal=Vector2(0, -1)):
        image = pygame.Surface((Paddle.width, Paddle.height), pygame.SRCALPHA)
        image.fill((255, 255, 255))
        super().__init__(camera, pos, image)
        self.normal = normal

    def update_image(self):
        vx = int(abs(self.velocity.x))
        factor = Paddle.height / Paddle.max_speed
        self.base_image = pygame.Surface((Paddle.width + vx,
                                          Paddle.height - vx * factor),
                                         pygame.SRCALPHA)
        self.base_image.fill((255, 255, 255))

    def update(self, mouse_pos):
        # self.vx = Paddle.clamp_speed((mouse_pos.x - self.pos.x) / 2)
        pos = self.camera.screen_to_world(mouse_pos)
        self.velocity.x = Paddle.clamp_speed((pos.x - self.pos.x)) / 1.1
        super().update()
        self.update_image()
