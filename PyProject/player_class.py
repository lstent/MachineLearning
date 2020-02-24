import pygame
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2,
                           (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2)
        print(self.grid_pos, self.pix_pos)

    def update(self):
        pass

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width//2-2)
