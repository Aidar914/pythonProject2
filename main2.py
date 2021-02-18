import pygame
import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.life = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, 'white', (self.left + (self.cell_size * i),
                                                   self.top + (self.cell_size * j),
                                                   self.cell_size, self.cell_size), width=1)

    def get_click(self, mouse_pos, mouse_button):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, mouse_button)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        sx = self.left + self.width * self.cell_size
        sy = self.top + self.height * self.cell_size
        if sx > x > self.left and sy > y > self.top:
            x -= self.left
            y -= self.top
            x = x // self.cell_size
            y = y // self.cell_size
            print(x, y)
            return x, y
        return None

    def on_click(self, cell, mouse_button):
        pass


class Minesweeper(Board):
    def __init__(self, width, height, mine):
        self.width = width
        self.height = height
        self.mine = mine
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.life = True
        self.win = False
        self.button = self.width * self.height - self.mine
        self.mine_true = self.mine
        b = []
        pygame.font.init()
        self.b1 = []
        self.b2 = []
        self.b3 = []
        for i in range(height):
            self.b1.append([0] * width)
        for i in range(height):
            self.b2.append([0] * width)
        for i in range(height):
            self.b3.append([0] * width)
        c = 0
        for i in range(mine + c):
            a = random.randint(0, width * height - 1)
            if a in b:
                c += 1
                continue
            b.append(a)
        for i in range(height):
            for j in range(width):
                if i * width + j in b:
                    self.b1[i][j] = 1
                    if i + 1 != height:
                        self.b2[i + 1][j] += 1
                        if j + 1 != width:
                            self.b2[i + 1][j + 1] += 1
                        if j - 1 >= 0:
                            self.b2[i + 1][j - 1] += 1
                    if i - 1 >= 0:
                        self.b2[i - 1][j] += 1
                        if j + 1 != width:
                            self.b2[i - 1][j + 1] += 1
                        if j - 1 >= 0:
                            self.b2[i - 1][j - 1] += 1
                    if j + 1 != width:
                        self.b2[i][j + 1] += 1
                    if j - 1 >= 0:
                        self.b2[i][j - 1] += 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.font = pygame.font.Font(None, self.cell_size + self.cell_size // 2)
        self.font1 = pygame.font.Font(None, 200)
        self.font2 = pygame.font.Font(None, 20)

    def render(self, screen):
        self.button = self.width * self.height - self.mine
        for i in range(self.height):
            for j in range(self.width):
                if self.b1[i][j] == 1:
                    if not self.life:
                        pygame.draw.rect(screen, 'red', ((self.top + (self.cell_size * i),
                                                          self.left + (self.cell_size * j),
                                                          self.cell_size, self.cell_size)))
                text = self.font.render(str(self.b2[i][j]), True, (0, 255, 0))
                if self.b3[i][j] == 1:
                    self.button -= 1
                    screen.blit(text, (self.top + self.cell_size * i + self.cell_size // 5, self.left + self.cell_size * j))
                pygame.draw.rect(screen, 'white', (self.top + (self.cell_size * i),
                                                   self.left + (self.cell_size * j),
                                                   self.cell_size, self.cell_size), width=1)
                if self.b3[i][j] == 2:
                    pygame.draw.rect(screen, 'blue', ((self.top + (self.cell_size * i),
                                                      self.left + (self.cell_size * j),
                                                      self.cell_size, self.cell_size)))
        if self.button == 0:
            self.win = True
            text = self.font1.render('YOU', True, (255, 0, 0))
            screen.blit(text, (120, 180, 400, 400))
            text = self.font1.render('WIN!', True, (255, 0, 0))
            screen.blit(text, (100, 300, 400, 450))
        if not self.life:
            text = self.font1.render('FALL', True, (255, 0, 0))
            screen.blit(text, (100, 180, 400, 400))
        text = self.font2.render('Количество бомб: ' + str(self.mine_true), True, (0, 255, 0))
        screen.blit(text, (10, 510, 500, 540))

    def on_click(self, cell, mouse_button):
        if self.life:
            if mouse_button == 1:
                x, y = cell
                if self.b3[x][y] != 2:
                    if self.b1[x][y] != 1 and self.b3[x][y] != 1:
                        if self.b2[x][y] == 0:
                            self.zero(x, y)
                        self.b3[x][y] = 1
                    if self.b1[x][y] == 1:
                        self.life = False
            elif mouse_button == 3:
                x, y = cell
                if self.b3[x][y] == 2:
                    self.b3[x][y] = 0
                    self.mine_true += 1
                elif self.b3[x][y] == 0:
                    self.b3[x][y] = 2
                    self.mine_true -= 1

    def zero(self, x, y):
        if x + 1 != self.width:
            if self.b2[x + 1][y] == 0 and self.b3[x + 1][y] == 0:
                self.b3[x + 1][y] = 1
                self.zero(x + 1, y)
            else:
                self.b3[x + 1][y] = 1
            if y != 0:
                if self.b2[x + 1][y - 1] == 0 and self.b3[x + 1][y - 1] == 0:
                    self.b3[x + 1][y - 1] = 1
                    self.zero(x + 1, y - 1)
                else:
                    self.b3[x + 1][y - 1] = 1
            if y + 1 != self.width:
                if self.b2[x + 1][y + 1] == 0 and self.b3[x + 1][y + 1] == 0:
                    self.b3[x + 1][y + 1] = 1
                    self.zero(x + 1, y + 1)
                else:
                    self.b3[x + 1][y + 1] = 1
        if x != 0:
            if self.b2[x - 1][y] == 0 and self.b3[x - 1][y] == 0:
                self.b3[x - 1][y] = 1
                self.zero(x - 1, y)
            else:
                self.b3[x - 1][y] = 1
            if y != 0:
                if self.b2[x - 1][y - 1] == 0 and self.b3[x - 1][y - 1] == 0:
                    self.b3[x - 1][y - 1] = 1
                    self.zero(x - 1, y - 1)
                else:
                    self.b3[x - 1][y - 1] = 1
            if y + 1 != self.width:
                if self.b2[x - 1][y + 1] == 0 and self.b3[x - 1][y + 1] == 0:
                    self.b3[x - 1][y + 1] = 1
                    self.zero(x - 1, y + 1)
                else:
                    self.b3[x - 1][y + 1] = 1
        if y + 1 != self.height:
            if self.b2[x][y + 1] == 0 and self.b3[x][y + 1] == 0:
                self.b3[x][y + 1] = 1
                self.zero(x, y + 1)
            else:
                self.b3[x][y + 1] = 1
            if x != 0:
                if self.b2[x - 1][y + 1] == 0 and self.b3[x - 1][y + 1] == 0:
                    self.b3[x - 1][y + 1] = 1
                    self.zero(x - 1, y + 1)
                else:
                    self.b3[x - 1][y + 1] = 1
            if x + 1 != self.height:
                if self.b2[x + 1][y + 1] == 0 and self.b3[x + 1][y + 1] == 0:
                    self.b3[x + 1][y + 1] = 1
                    self.zero(x + 1, y + 1)
                else:
                    self.b3[x + 1][y + 1] = 1
        if y != 0:
            if self.b2[x][y - 1] == 0 and self.b3[x][y - 1] == 0:
                self.b3[x][y - 1] = 1
                self.zero(x, y - 1)
            else:
                self.b3[x][y - 1] = 1
            if x != 0:
                if self.b2[x - 1][y - 1] == 0 and self.b3[x - 1][y - 1] == 0:
                    self.b3[x - 1][y - 1] = 1
                    self.zero(x - 1, y - 1)
                else:
                    self.b3[x - 1][y - 1] = 1
            if x + 1 != self.width:
                if self.b2[x + 1][y - 1] == 0 and self.b3[x + 1][y - 1] == 0:
                    self.b3[x + 1][y - 1] = 1
                    self.zero(x + 1, y - 1)
                else:
                    self.b3[x + 1][y - 1] = 1


def main():
    size = width, height = 509, 600
    screen = pygame.display.set_mode(size)
    mine = Minesweeper(10, 10, 20)
    mine.set_view(5, 5, 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mine.get_click(event.pos, event.button)
        screen.fill((0, 0, 0))
        mine.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
