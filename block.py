
import pygame
from game_object import GameObject
from vector import Vector2
from random import randrange


class Block(GameObject):

    width = 50
    height = 20
    color = lambda: (randrange(128, 256),
                     randrange(128, 256),
                     randrange(128, 256),
                     255)

    def __init__(self, camera, pos):
        image = pygame.Surface((Block.width, Block.height), pygame.SRCALPHA)
        self.color = Block.color()
        image.fill(self.color)
        super().__init__(camera, pos, image)

    def get_side(self, ball):
        if ball.pos.x > self.pos.x:
            if ball.rect.left < self.rect.right:
                return Vector2(0, 1 if ball.pos.y > self.pos.y else -1)
            else:
                return Vector2(1, 0)
        else:
            if ball.rect.right > self.rect.left:
                return Vector2(0, 1 if ball.pos.y > self.pos.y else -1)
            else:
                return Vector2(-1, 0)


class DeadBlock(GameObject):

    x_vel = lambda: randrange(-10, +10)
    y_vel = lambda: randrange(-20, -10)
    angle_vel = lambda: randrange(-20, +20)
    gravity = 2

    def __init__(self, camera, block, velocity=None):
        super().__init__(camera, block.pos, block.image)
        if velocity:
            self.velocity = velocity
        else:
            self.velocity = Vector2(DeadBlock.x_vel(), DeadBlock.y_vel())
        self.angle_speed = DeadBlock.angle_vel()
        self.color = block.color

    def update(self, screen_height):
        super().update()
        self.velocity += Vector2(0, DeadBlock.gravity)
        self.angle += self.angle_speed
        r, g, b, a = self.color
        a *= 0.9
        self.color = r, g, b, a
        self.base_image.fill(self.color)
        if self.rect.top > screen_height or a < 1:
            self.kill()
