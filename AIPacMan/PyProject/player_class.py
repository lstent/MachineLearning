import pygame
from settings import *
vec = pygame.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec()
        self.target = vec()
        self.current_score = 0
        self.speed = 2
        self.cell_row = 1
        self.lives = 3
        self.cheapest_cell = 1000
        self.starting_pos = [pos.x, pos.y]

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            if self.target is None:
                pass
            if self.target is not None:
                self.pix_pos += self.direction * self.speed
                if self.time_to_move():
                    self.move()
                    # the output values will be an array of player positions
                    # self.app.ws.cell(row=self.cell_row + 1, column=1, value=self.pix_pos.x)
                    self.app.ws.cell(row=self.cell_row + 1, column=26, value=self.key_press_direction())
                    self.cell_row = self.cell_row + 1
        self.cheapest_cell = 1000
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width//2)//self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height//2) // self.app.cell_height + 1
        if self.on_coin():
            self.eat_coin()

    def set_target(self):
        closest_cell_vec = None
        for cell in self.app.grid_tiles:
            if (self.grid_pos[0] + 2) >= cell.grid_pos.x >= (self.grid_pos[0] - 2) and (self.grid_pos[1] + 2) >= \
                    cell.grid_pos.y >= (self.grid_pos[1] - 2) and not self.grid_pos == cell.grid_pos:
                if cell.value < self.cheapest_cell:
                    self.cheapest_cell = cell.value
                    closest_cell_vec = cell.grid_pos
        return closest_cell_vec

    def move(self):
        self.direction = self.get_path_direction(self.target)

    def get_path_direction(self, target):
        next_cell = self.find_next_cell_in_path(target)
        if target is None:
            pass
        if target is not None:
            xdir = next_cell[0] - self.grid_pos[0]
            ydir = next_cell[1] - self.grid_pos[1]
            return vec(xdir, ydir)

    def find_next_cell_in_path(self, target):
        if target is None:
            pass
        if target is not None:
            path = self.BFS([int(self.grid_pos[0]), int(self.grid_pos[1])], [int(target.x), int(target.y)])
            return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
                        if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
                            next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def draw(self):
        pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (int(self.pix_pos.x), int(self.pix_pos.y)),
                           self.app.cell_width//2-2)

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, PLAYER_COLOUR, (30 + 20*x, HEIGHT - 15), 7)

        # Drawing the grid pos rect
        #pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER//2,
                                                #self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER//2,
                                                #self.app.cell_width, self.app.cell_height), 1)

    def on_coin(self):
        if self.grid_pos in self.app.coins:
            if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)
        self.current_score += 1

    def get_pix_pos(self):
        return vec((self.grid_pos[0] * self.app.cell_width) + TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2,
                   (self.grid_pos[1] * self.app.cell_height) + TOP_BOTTOM_BUFFER//2 + self.app.cell_height//2)

    def time_to_move(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER//2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def key_press_direction(self):
        if self.direction == vec(0, 1):
            return "down"
        if self.direction == vec(0, -1):
            return "up"
        if self.direction == vec(1, 0):
            return "right"
        if self.direction == vec(-1, 0):
            return "left"
