import pygame
from settings import *

vec = pygame.math.Vector2


class Grid:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.number = number
        self.value = 0
        self.radius = int(self.app.cell_width//2.3)
        self.enemy_distance_0 = int()
        self.enemy_distance_1 = int()
        self.enemy_distance_2 = int()
        self.enemy_distance_3 = int()
        self.cell_row = 1
        self.cell_column = 1

    def update(self):
        coin = self.app.coins.count(self.grid_pos)
        self.cell_row = self.app.player.cell_row
        player_distance = (int(abs(self.grid_pos.x - self.app.player.grid_pos.x) + abs(self.grid_pos.y -
                                                                                       self.app.player.grid_pos.y)))
        if (self.app.player.grid_pos.x + 5) >= self.grid_pos.x >= (self.app.player.grid_pos.x - 5) and (
                self.app.player.grid_pos.y + 5) >= self.grid_pos.y >= (self.app.player.grid_pos.y - 5) and not \
                self.app.player.grid_pos == self.grid_pos:
            if coin == 1:
                self.value = int(abs((player_distance / 2) + self.get_enemy_distance_0() + self.get_enemy_distance_1()
                                     + self.get_enemy_distance_2() + self.get_enemy_distance_3()))
            elif coin == 0:
                self.value = int(abs(player_distance + self.get_enemy_distance_0() + self.get_enemy_distance_1() +
                                     self.get_enemy_distance_2() + self.get_enemy_distance_3())+10)
            self.app.ws.cell(row=self.cell_row + 1, column=self.cell_column + 1, value=self.value)
            if self.cell_column == 24:
                self.cell_column = 0
            else:
                self.cell_column = self.cell_column + 1
            self.app.wb.save('pacman.xlsx')

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + TOP_BOTTOM_BUFFER // 2 + self.app.cell_height // 2)

    def get_enemy_distance_0(self):
        enemy = self.app.enemies[0]
        if int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y - enemy.grid_pos.y)) == 0:
            self.enemy_distance_0 = 99
        else:
            self.enemy_distance_0 = 99 / (int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y -
                                                                                            enemy.grid_pos.y)))
        return self.enemy_distance_0

    def get_enemy_distance_1(self):
        enemy = self.app.enemies[1]
        if int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y - enemy.grid_pos.y)) == 0:
            self.enemy_distance_1 = 99
        else:
            self.enemy_distance_1 = 99 / (int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y -
                                                                                            enemy.grid_pos.y)))
        return self.enemy_distance_1

    def get_enemy_distance_2(self):
        enemy = self.app.enemies[2]
        if int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y - enemy.grid_pos.y)) == 0:
            self.enemy_distance_2 = 99
        else:
            self.enemy_distance_2 = 99 / (int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y -
                                                                                            enemy.grid_pos.y)))
        return self.enemy_distance_2

    def get_enemy_distance_3(self):
        enemy = self.app.enemies[3]
        if int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y - enemy.grid_pos.y)) == 0:
            self.enemy_distance_3 = 99
        else:
            self.enemy_distance_3 = 99 / (int(abs(self.grid_pos.x - enemy.grid_pos.x) + abs(self.grid_pos.y -
                                                                                            enemy.grid_pos.y)))
        return self.enemy_distance_3

    def draw(self):
        if (self.app.player.grid_pos.x + 5) >= self.grid_pos.x >= (self.app.player.grid_pos.x - 5) and (
                self.app.player.grid_pos.y + 5) >= self.grid_pos.y >= (self.app.player.grid_pos.y - 5) and not \
                self.app.player.grid_pos == self.grid_pos:
            self.draw_text(
                '{}'.format(self.value),
                self.app.screen, [int(self.grid_pos.x * self.app.cell_width) + self.app.cell_width // 2 +
                                  TOP_BOTTOM_BUFFER // 2, int(self.grid_pos.y * self.app.cell_height) +
                                  self.app.cell_height // 2 + TOP_BOTTOM_BUFFER // 2], 9, RED, START_FONT)


