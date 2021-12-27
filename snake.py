from enum import Enum
import pygame
import random
from collections import namedtuple
import numpy as np

pygame.init()


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Colors(Enum):
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 102)
    BLACK = (40, 40, 40)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    BLUE = (50, 153, 213)


snake_size = 10
font = pygame.font.SysFont()
snake_speed = 20

coordinate = namedtuple('Point', 'x_cor, y_cor')


class Snake:

    def __init__(self, width=600, height=400):
        self.width = width
        self.height = height

        # render display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kodutöö 7")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # restart game state
        self.direction = Direction.UP

        # Reset all variables
        self.head = coordinate(self.width / 2, self.height / 2)
        self.snake = [self.head]

        self.score = 0
        self.food = None
        self._place_food()
        self.current_frame = 0

    def _place_food(self):
        foodx = round(random.randrange(0, self.width - snake_size) / snake_size) * snake_size
        foody = round(random.randrange(0, self.height - snake_size) / snake_size) * snake_size
        self.food = coordinate(foodx, foody)

        # If the place where food is placed is the same as the head,
        # then generate new coordinates for the food
        if self.food in self.snake:
            self._place_food()

    def is_death(self):
        currentHead = self.head

        # Goes into the wall
        if currentHead.x_cor > self.width - snake_size or currentHead.x_cor < 0 or currentHead.y_cor < 0 or currentHead.y_cor > self.height - snake_size:
            return True

        # Goes into itself
        if currentHead in self.snake[1:]:
            return True

        return False

    def _move(self, action):
        # since we cant turn the snake around, then the only options for the snake
        # to do at once is to either turn left, right or go straight
        # the possible actions are [straight, left, right], so
        # [1, 0, 0] is straight, [0,1,0] is left, [0, 0, 1] is right

        movements = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        currentIdx = movements.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            # if we want to go straight, then no change
            new_direction = movements[currentIdx]
        elif np.array_equal(action, [0, 1, 0]):
            # we want to go left
            next_idx = (currentIdx + 1) % 4
            new_direction = movements[next_idx]
        else:  # [0, 0, 1]
            next_idx = (currentIdx - 1) % 4
            new_direction = movements[next_idx]

        self.direction = new_direction

        headX = self.head.x_cor
        headY = self.head.y_cor

        if self.direction == Direction.UP:
            headY -= snake_size
        elif self.direction == Direction.DOWN:
            headY += snake_size
        elif self.direction == Direction.LEFT:
            headX -= snake_size
        elif self.direction == Direction.RIGHT:
            headX += snake_size

        self.head = coordinate(headX, headY)


    def _refresh_ui(self):
        self.display.fill(Colors.BLACK)

        for coordinate in self.snake:
            pygame.draw.rect(self.display, Colors.GREEN, pygame.Rect(coordinate.x_cor, coordinate.y_cor, snake_size, snake_size))

        pygame.draw.rect(self.display, Colors.BLUE, pygame.Rect(self.food.x_cor, self.food.y_cor, snake_size, snake_size))

        renderScore = font.render("Score: " + str(self.score), Colors.WHITE)

        self.display.blit(renderScore, [0, 0])
        pygame.display.flip()

    def play_step(self, action):
        # move the snake 1 step forward
        self.current_frame += 1

        self._move(action)
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False

        if self.is_death() or self.current_frame > 50 * len(self.snake):
            #Check if dead or the game has already lasted for too long.

            game_over = True
            reward = -10

            return reward, game_over, self.score

        # Move or place food
        if self.food == self.head:
            self.score += 1
            reward = 30
            self._place_food()
        else:
            self.snake.pop()

        self._refresh_ui()
        self.clock.tick(snake_speed)

        return reward, game_over, self.score



