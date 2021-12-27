from collections import deque
import random

from snake import Direction, Snake, coordinate, SNAKE_SIZE
import numpy as np
import tensorflow
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense

MEM_SIZE = 100_000


class Agent:
    def __init__(self):
        self.num_games = 0
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.95
        self.batch_size = 500
        self.memory = deque(maxlen=MEM_SIZE)
        self.learning_rate = 0.00025
        self.input_size = 11
        self.output_size = 3
        self._build_model()

    def _build_model(self):
        model = Sequential()
        # Input
        model.add(Input(shape=(self.input_size,)))

        # Hidden
        model.add(Dense(128, activation="relu"))
        model.add(Dense(128, activation="relu"))

        # Output
        model.add(Dense(self.output_size, activation="softmax"))
        model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))
        self.model = model

    def get_state(self, snake: Snake):
        head = snake.snake[0]

        # Points around head of the snake
        point_left = coordinate(head.x_cor - SNAKE_SIZE, head.y_cor)
        point_right = coordinate(head.x_cor + SNAKE_SIZE, head.y_cor)
        point_up = coordinate(head.x_cor, head.y_cor - SNAKE_SIZE)
        point_down = coordinate(head.x_cor, head.y_cor + SNAKE_SIZE)

        # Which dir snake is moving
        is_dir_left = snake.direction == Direction.LEFT
        is_dir_right = snake.direction == Direction.RIGHT
        is_dir_up = snake.direction == Direction.UP
        is_dir_down = snake.direction == Direction.DOWN

        state = [
            # Death straight
            (is_dir_right and snake.is_death(point_right))
            or (is_dir_left and snake.is_death(point_left))
            or (is_dir_up and snake.is_death(point_up))
            or (is_dir_down and snake.is_death(point_down)),
            # Death right
            (is_dir_up and snake.is_death(point_right))
            or (is_dir_down and snake.is_death(point_left))
            or (is_dir_left and snake.is_death(point_up))
            or (is_dir_right)
            and snake.is_death(point_down),
            # Death left
            (is_dir_down and snake.is_death(point_right))
            or (is_dir_left and snake.is_death(point_down))
            or (is_dir_up and snake.is_death(point_left))
            or (is_dir_right and snake.is_death(point_up)),
            # Movement direction as bools
            is_dir_up,
            is_dir_right,
            is_dir_down,
            is_dir_right,
            # Food loc
            snake.food.y_cor < snake.head.y_cor,  # up
            snake.food.x_cor > snake.head.x_cor,  # right
            snake.food.y_cor > snake.head.y_cor,  # down
            snake.food.x_cor < snake.head.x_cor,  # left
        ]

        assert self.input_size == len(state)

        return np.array(state, dtype=np.float32)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def get_action(self, state):
        move = [0, 0, 0]

        # Predict randomly at the start
        if np.random.rand() <= self.epsilon:
            idx = random.randint(0, 2)
        else:
            prediction = self.model(np.array([state]))
            idx = np.argmax(prediction)

        move[idx] = 1
        return move

    def train_memory(self):

        # Only train memory if enough memories have been accumulated
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        game_overs = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = []
        predictions = self.model.predict_on_batch(next_states)
        for i in range(self.batch_size):
            target = np.amax(predictions[i])

            # Amplify the models prediction based on the results of the generation
            target = rewards[i] + self.gamma * target * (1 - game_overs[i])
            targets.append(target)

        y = self.model.predict_on_batch(states)

        # Replace predictions with modified predictions on next states
        # Replace the value that was actually used based on an action
        for i in range(self.batch_size):
            idx = np.argmax(actions[i])
            y[i][idx] = targets[i]

        self.model.fit(states, y, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
