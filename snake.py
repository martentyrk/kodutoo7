import pygame
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (40, 40, 40)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Kodutöö 7 snake game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 10

font_style = pygame.font.SysFont("bahnschrift", 25)

def score_keeper(score):
    value = font_style.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def render_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    x_coordinate = dis_width / 2
    y_coordinate = dis_height / 2

    x_speed = 0
    y_speed = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Kaotasid! Vajuta A klahvi, et uuesti mängida ning Q klahvi, et mäng sulgeda", red)
            score_keeper(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_a:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_block
                    y_speed = 0
                elif event.key == pygame.K_RIGHT:
                    x_speed = snake_block
                    y_speed = 0
                elif event.key == pygame.K_UP:
                    y_speed = -snake_block
                    x_speed = 0
                elif event.key == pygame.K_DOWN:
                    y_speed = snake_block
                    x_speed = 0

        #Check if the snake has hit the wall.
        if x_coordinate >= dis_width or x_coordinate < 0 or y_coordinate >= dis_height or y_coordinate < 0:
            game_close = True
        x_coordinate += x_speed
        y_coordinate += y_speed
        dis.fill(black)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = []
        snake_head.append(x_coordinate)
        snake_head.append(y_coordinate)
        snake_list.append(snake_head)

        #Hold only the snake boxes in the list that are needed.
        if len(snake_list) > length_of_snake:
            del snake_list[0]


        #Check if snake bumps into itself
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        render_snake(snake_block, snake_list)
        score_keeper(length_of_snake - 1)

        pygame.display.update()

        #If on top of food, then eat.
        if x_coordinate == foodx and y_coordinate == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        #Clock makes the game run slower, otherwise it would be impossible to play.
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()