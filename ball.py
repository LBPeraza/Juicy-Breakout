
import pygame
from game_object import GameObject


class Ball(GameObject):

    size = 10
    start_speed = 10

    def __init__(self, camera, pos):
        image = pygame.Surface((Ball.size, Ball.size))
        image.fill((255, 255, 255))
        super().__init__(camera, pos, image)

    def launch(self, direction):
        self.velocity = direction

    def bounce(self, normal):
        proj = normal * (self.velocity.dot(normal) / normal.size_squared)
        self.velocity -= 2 * proj

    def track_to_paddle(self, paddle):
        scale = (paddle.image.get_height() + Ball.size) / 2
        self.pos = paddle.pos + paddle.normal * scale

    def update(self, left, right, top, bottom, track_paddle=None):
        if track_paddle:
            self.track_to_paddle(track_paddle)
        else:
            if self.rect.left < left:
                self.velocity.x *= -1
                self.pos.x = left + self.rect.width // 2
            elif self.rect.right > right:
                self.velocity.x *= -1
                self.pos.x = right - self.rect.width // 2
            if self.rect.top < top:
                self.velocity.y *= -1
                self.pos.y = top + self.rect.height // 2
            elif self.rect.bottom > bottom:
                self.velocity.y *= -1
                self.pos.y = bottom - self.rect.height // 2
        super().update()
