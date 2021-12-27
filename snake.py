from enum import Enum
import pygame
import random
from collections import namedtuple
import numpy as np
import math

pygame.init()

DEATH_REWARD = -10
FOOD_REWARD = 30


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


SNAKE_SIZE = 10
font = pygame.font.SysFont("Arial", 16)
SNAKE_SPEED = 20

coordinate = namedtuple("Point", "x_cor, y_cor")


class Snake:
    def __init__(self, generation, width=600, height=400):
        self.width = width
        self.height = height
        self.generation = generation
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
        foodx = (
            round(random.randrange(0, self.width - SNAKE_SIZE) / SNAKE_SIZE)
            * SNAKE_SIZE
        )
        foody = (
            round(random.randrange(0, self.height - SNAKE_SIZE) / SNAKE_SIZE)
            * SNAKE_SIZE
        )
        self.food = coordinate(foodx, foody)

        # If the place where food is placed is the same as the head,
        # then generate new coordinates for the food
        if self.food in self.snake:
            self._place_food()

    def is_death(self, point: coordinate = None):
        if point is None:
            point = self.head

        # Goes into the wall
        if (
            point.x_cor > self.width - SNAKE_SIZE
            or point.x_cor < 0
            or point.y_cor < 0
            or point.y_cor > self.height - SNAKE_SIZE
        ):
            return True

        # Goes into itself
        if point in self.snake[1:]:
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
            headY -= SNAKE_SIZE
        elif self.direction == Direction.DOWN:
            headY += SNAKE_SIZE
        elif self.direction == Direction.LEFT:
            headX -= SNAKE_SIZE
        elif self.direction == Direction.RIGHT:
            headX += SNAKE_SIZE

        self.head = coordinate(headX, headY)

    def _refresh_ui(self):
        self.display.fill(Colors.BLACK.value)

        for coordinate in self.snake:
            pygame.draw.rect(
                self.display,
                Colors.GREEN.value,
                pygame.Rect(coordinate.x_cor, coordinate.y_cor, SNAKE_SIZE, SNAKE_SIZE),
            )

        pygame.draw.rect(
            self.display,
            Colors.BLUE.value,
            pygame.Rect(self.food.x_cor, self.food.y_cor, SNAKE_SIZE, SNAKE_SIZE),
        )

        renderScore = font.render("Score: " + str(self.score), True, Colors.WHITE.value)
        render_generation = font.render(
            "Generation: " + str(self.generation), True, Colors.WHITE.value
        )

        self.display.blit(renderScore, [0, 0])
        self.display.blit(
            render_generation, [self.width - render_generation.get_width(), 0]
        )
        pygame.display.flip()

    def play_step(self, action):
        # move the snake 1 step forward
        self.current_frame += 1

        dist_before_move = math.sqrt(
            (self.food.x_cor - self.head.x_cor) ** 2
            + (self.food.y_cor - self.head.y_cor) ** 2
        )

        self._move(action)
        dist_after_move = math.sqrt(
            (self.food.x_cor - self.head.x_cor) ** 2
            + (self.food.y_cor - self.head.y_cor) ** 2
        )

        self.snake.insert(0, self.head)
        reward = 0

        if dist_after_move < dist_before_move:
            reward += 1
        else:
            reward -= 1

        game_over = False

        if self.is_death() or self.current_frame > 50 * len(self.snake):
            # Check if dead or the game has already lasted for too long.

            game_over = True
            reward += DEATH_REWARD

            return reward, game_over, self.score

        # Move or place food
        if self.food == self.head:
            self.score += 1
            reward += FOOD_REWARD
            self._place_food()
        else:
            self.snake.pop()

        self._refresh_ui()
        self.clock.tick(SNAKE_SPEED)

        return reward, game_over, self.score
