"""
Space Invaders Game

This script initializes and runs the Space Invaders game using the Pygame library.
"""

import pygame
from source import SpaceInvadersGame

pygame.init()

if __name__ == "__main__":
    game = SpaceInvadersGame()

    while True:
        game_over = game.play_step()

        if game_over:
            break

    print(f"Game ended")
pygame.quit()
