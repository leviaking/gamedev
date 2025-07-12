import pettingzoo
from pettingzoo.classic import connect_four_v3
import pygame
import time

# Initialize the Connect Four environment
env = connect_four_v3.env()

# Reset the environment to start a new game
env.reset()

# Initialize pygame for rendering
pygame.init()
screen = pygame.display.set_mode((env.width * 60, env.height * 60))  # Adjust size as needed
pygame.display.set_caption("Connect Four")

# Main game loop
while env.agents:
    current_agent = env.agent_selection()
    observation, reward, termination, truncation, info = env.step(env.action_space(current_agent).sample()) # or use a trained agent here.
    env.render() # Render the game state

    # Pygame rendering
    board = env.board
    for r in range(env.height):
        for c in range(env.width):
            x = c * 60
            y = r * 60
            pygame.draw.rect(screen, (0, 0, 0), (x, y, 60, 60), 2)  # Draw grid
            if board[r, c] == 1:  # Player 1
                pygame.draw.circle(screen, (255, 0, 0), (x + 30, y + 30), 25)
            elif board[r, c] == 2:  # Player 2
                pygame.draw.circle(screen, (255, 255, 0), (x + 30, y + 30), 25)

    pygame.display.flip()  # Update the display

    time.sleep(0.2)  # Adjust delay for visualization speed

    if termination or truncation:
        break

pygame.quit()  # Close pygame window

# Print the results of the game after it is finished.
if termination:
    print(f"Game over! Winner: {env.rewards[current_agent]}")
elif truncation:
    print("Game truncated!")
else:
    print("Game finished normally.")