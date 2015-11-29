
import pygame
from vector import Vector2


class GameObject(pygame.sprite.Sprite):
    def __init__(self, camera, pos, image):
        super().__init__()
        self.pos = pos
        self.image = image
        self.base_image = image.copy()
        self.angle = 0
        self.velocity = Vector2(0, 0)
        self.camera = camera
        self.update_rect()

    def update_rect(self):
        width, height = self.image.get_size()
        x, y = self.camera.world_to_screen(self.pos)
        self.rect = pygame.Rect(x - width / 2, y - height / 2,
                                width, height)

    def update(self):
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.pos += self.velocity
        self.update_rect()
