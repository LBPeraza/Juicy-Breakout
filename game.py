
import pygame
from vector import Vector2
from pygame_game import PygameGame
from paddle import Paddle
from block import Block, DeadBlock
from ball import Ball
from camera import Camera
from constants import *
import random


class Game(PygameGame):
    def random_blocks(self, max_y, count=20, stop=5):
        randint = random.randint
        blocks = pygame.sprite.Group()
        x = lambda: randint(Block.width // 2, self.width - Block.width // 2)
        y = lambda: randint(Block.height // 2, max_y - Block.height // 2)
        fails = 0
        while len(blocks) < count and fails < stop:
            block = Block(self.camera, Vector2(x(), y()))
            if pygame.sprite.spritecollideany(block, blocks):
                fails += 1
            else:
                fails = 0
                blocks.add(block)
        return blocks

    def structured_blocks(self, rows=4, cols=6):
        width = Block.width * cols
        x_margin = (self.width - width) // (cols + 1)
        height = Block.height * rows
        y_margin = (self.height // 2 - height) // (rows + 1)
        x0 = x_margin + Block.width // 2
        y0 = y_margin + Block.height // 2
        blocks = pygame.sprite.Group()
        for row in range(rows):
            y = y0 + row * (Block.height + y_margin)
            for col in range(cols):
                x = x0 + col * (Block.width + x_margin)
                blocks.add(Block(self.camera, Vector2(x, y)))
        return blocks

    def init(self):
        self.camera = Camera(self.width, self.height,
                             Vector2(self.width // 2, self.height // 2))
        self.blocks = self.structured_blocks(5, 5)
        self.dead_blocks = pygame.sprite.Group()
        self.bg_color = (0, 0, 0)
        self.paddle = pygame.sprite.GroupSingle(
            Paddle(self.camera, Vector2(self.width / 2,
                                        self.height - Paddle.height)))
        self.ball = pygame.sprite.GroupSingle(
            Ball(self.camera, Vector2(self.width / 2, self.height / 2)))
        self.mouse_pos = None
        self.track_paddle = self.paddle.sprite
        self.ball.sprite.track_to_paddle(self.track_paddle)
        self.camera_v = Vector2(0, 0)
        self.inverted = False

    def mousePressed(self, x, y):
        block = Block(self.camera, Vector2(x, y))
        collide = pygame.sprite.spritecollideany(block, self.blocks)
        if collide:
            self.kill_block(collide)
        else:
            self.blocks.add(block)

    def kill_block(self, block, velocity=None):
        if JUICE[0]:
            self.dead_blocks.add(DeadBlock(self.camera, block, velocity))
        block.kill()

    def mouseMotion(self, x, y):
        self.mouse_pos = Vector2(x, y)

    def keyPressed(self, key, mod):
        if key == pygame.K_SPACE and self.track_paddle:
            # vx = 2 * self.track_paddle.velocity.x / Paddle.max_speed
            velocity = self.track_paddle.normal
            self.ball.sprite.launch(velocity * Ball.start_speed)
            self.track_paddle = None
        elif key == pygame.K_r:
            self.init()
        elif key == pygame.K_j:
            JUICE[0] = not JUICE[0]
            for block in self.blocks:
                block.recolor(None if JUICE[0] else (255, 255, 255, 255))

    def ball_block_collide(self):
        collide = pygame.sprite.spritecollideany(self.ball.sprite, self.blocks)
        rand = lambda: ((lambda x: x if random.randint(0, 1) else -x)
                        (random.randint(5, 10)))
        if collide:
            side = collide.get_side(self.ball.sprite)
            self.kill_block(collide, self.ball.sprite.velocity)
            self.ball.sprite.bounce(side)
            if JUICE[0]:
                self.camera.move(Vector2(rand(), rand()))
                self.inverted = True

    def ball_paddle_collide(self):
        collide = pygame.sprite.spritecollideany(self.ball.sprite, self.paddle)
        if collide:
            diff = self.ball.sprite.pos - self.paddle.sprite.pos
            diff.x /= 3
            diff.x += random.randint(-1, 1)
            self.ball.sprite.launch(diff.normalized() * Ball.start_speed)

    def update_camera_vel(self):
        want = Vector2(self.width // 2, self.height // 2)
        self.camera_v *= 0.05
        self.camera_v += 0.8 * (want - self.camera.center)

    def timerFired(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.paddle.update(Vector2(*mouse_pos))
        self.blocks.update()
        self.dead_blocks.update(self.height)
        self.ball_block_collide()
        if self.track_paddle is None:
            self.ball_paddle_collide()
        self.ball.update(0, self.width, 0, self.height, self.track_paddle)
        self.update_camera_vel()
        self.camera.move(self.camera_v)

    def redrawAll(self, screen):
        self.paddle.draw(screen)
        self.blocks.draw(screen)
        self.dead_blocks.draw(screen)
        self.ball.draw(screen)
        if self.inverted:
            inv = pygame.Surface((self.width, self.height))
            inv.fill((255, 255, 255))
            rect = (0, 0, self.width, self.height)
            inv.blit(screen, rect, None, pygame.BLEND_RGB_SUB)
            screen.blit(inv, rect)
            self.inverted = False


Game().run()
