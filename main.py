from snake import Colors, Snake
from agent import Agent


def train():
    all_scores = []
    gens = 50
    agent = Agent()
    for g in range(gens):
        snake = Snake(generation=g)
        score = 0
        # In case the agent starts moving the snake in a loop for example
        max_iterations = 10_000
        for i in range(max_iterations):
            # Get old state
            prev_state = agent.get_state(snake)

            # Get action
            action = agent.get_action(prev_state)

            # Play a move and get new state
            reward, game_over, snake_score = snake.play_step(action)
            next_state = agent.get_state(snake)

            # remember
            agent.remember(prev_state, action, reward, next_state, game_over)

            score += snake_score

            # Train memory
            agent.train_memory()

            if game_over:
                print(f"final state before dying: {prev_state}")
                print(f"generation: {g}, score: {score}")
                snake.reset()

                agent.num_games += 1
                break
        all_scores.append(score)

    return all_scores


if __name__ == "__main__":
    train()
