import requests
import os
import pygame


# кнопки q w e меняет режим карты


def draw():
    global x
    global y
    if x >= 180:
        x = -179
    if x <= -179:
        x = 180
    if s > 80:
        y = 0
    if y + s > 90:
        y = 90 - s
    elif y < 0 and -y + s > 90:
        y = -1 * (90 - s)
    if r == 1:
        return f"http://static-maps.yandex.ru/1.x/?ll={x},{y}" \
               f"&spn={s},{s}&l=map"
    if r == 2:
        return f"http://static-maps.yandex.ru/1.x/?ll={x},{y}" \
               f"&spn={s},{s}&l=sat"
    if r == 3:
        return f"http://static-maps.yandex.ru/1.x/?ll={x},{y}" \
               f"&spn={s},{s}&l=sat,skl"


def draw1():
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (200, 200, 200), (500, 25, 75, 40))
    pygame.draw.rect(screen, 'black', (500, 25, 75, 40), width=2)
    pygame.draw.rect(screen, 'black', (0, 100, 600, 450), width=5)
    if d:
        pygame.draw.rect(screen, (200, 200, 200), (10, 25, 475, 40))
    if f:
        pygame.draw.rect(screen, (100, 200, 200), (10, 25, 475, 40))
    pygame.draw.rect(screen, 'black', (10, 25, 475, 40), width=2)
    screen.blit(pygame.image.load(map_file), (0, 100))
    font = pygame.font.Font(None, 20)
    text = font.render("Искать", True, (0, 0, 0))
    screen.blit(text, (515, 38, 75, 40))
    text = font.render(word, True, (0, 0, 0))
    screen.blit(text, (20, 38, 75, 40))
    pygame.display.flip()


x, y, s = list(map(float, input().split()))
clock1 = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((600, 550))
r = 1
word = ''
d = False
f = False
running = True
map_request = draw()
response = requests.get(map_request)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
draw1()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 10 < x < 485 and 25 < y < 75:
                d = True
                draw1()
            elif d and 500 < x < 575 and 25 < y < 75:
                f = True
            else:
                d = False
                draw1()
        if event.type == pygame.KEYDOWN:
            if not d:
                print(event.key)
                if event.key == 113:
                    r = 1
                    map_request = draw()
                if event.key == 119:
                    r = 2
                    map_request = draw()
                if event.key == 101:
                    r = 3
                    map_request = draw()
                if event.key == 1073741906:
                    if s > 20:
                        y += 5
                    if s > 5:
                        y += 1
                    map_request = draw()
                if event.key == 1073741905:
                    if s > 20:
                        y -= 5
                    if s > 5:
                        y -= 1
                    map_request = draw()
                if event.key == 1073741904:
                    if s > 20:
                        x -= 5
                    elif s > 5:
                        x -= 1
                    else:
                        x -= 0.5
                    map_request = draw()
                if event.key == 1073741903:
                    if s > 20:
                        x += 5
                    elif s > 5:
                        x += 1
                    else:
                        x += 0.5
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
                response = requests.get(map_request)
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                draw1()
            else:
                print(event.key)
                if 122 >= event.key >= 97:
                    word += chr(event.key)
                    print(word)
                elif event.key == 8:
                    word = word[0:-1]
                    print(word)
                elif event.key == 32:
                    word += ' '
                elif 48 <= event.key <= 57:
                    word += chr(event.key)
                    print(chr(event.key))
                if len(word) >= 60:
                    word = word[0:-1]
    draw1()
    clock1.tick(10)
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
