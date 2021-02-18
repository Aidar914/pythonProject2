import time
import requests
import os
import pygame


def draw():
    global x
    global y
    if s > 80:
        x = 0
        y = 0
    if y + s > 90:
        y = s - 90
    elif y < 0 and y == 0:
        pass
    return f"http://static-maps.yandex.ru/1.x/?ll={x},{y}" \
           f"&spn={s},{s}&l=sat"


x, y, s = list(map(float, input().split()))
clock1 = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((600, 450))
i = 0
running = True
map_request = draw()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == 1073741906:
                y += 1
                map_request = draw()
            if event.key == 1073741899:
                if s < 10:
                    s += 0.5
                    map_request = draw()
                elif s < 88:
                    s += 1
                    map_request = draw()
            if event.key == 1073741902:
                if s > 1:
                    s -= 1
                    map_request = draw()
                if 1 > s > 0.1:
                    s -= 0.1
                    map_request = draw()
    if i % 10 == 0:
        response = requests.get(map_request)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
    i += 1
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    clock1.tick(10)
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
