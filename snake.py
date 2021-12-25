import pygame

pygame.init()

white_color = (255, 255, 255)
black_color = (0, 0, 0)
green_color = (255, 0, 0)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Kodutoo 7 snake')

game_over = False

x1 = dis_width / 2
y1 = dis_height / 2

snake_size = 10

x1_speed = 0
y1_speed = 0
clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_speed = -snake_size
                y1_speed = 0
            elif event.key == pygame.K_RIGHT:
                x1_speed = snake_size
                y1_speed = 0
            elif event.key == pygame.K_UP:
                y1_speed = -snake_size
                x1_speed = 0
            elif event.key == pygame.K_DOWN:
                y1_speed = snake_size
                x1_speed = 0

    if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
        game_over = True


    x1 += x1_speed
    y1 += y1_speed
    dis.fill(white_color)
    pygame.draw.rect(dis, green_color, [x1, y1, snake_size, snake_size])

    pygame.display.update()

    clock.tick(30)
pygame.quit()
quit()