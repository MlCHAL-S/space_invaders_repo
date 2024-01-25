"""
Constants for Space Invaders Game

This module defines a collection of constants used in the Space Invaders game implemented using Pygame.
These constants are used for setting up the game's display properties, defining gameplay mechanics,
and initializing key game attributes. This centralization of constants ensures consistency and ease
of modifications throughout the game's codebase.

"""
# Color definitions used in the game
WHITE = (255, 255, 255)  # Color for general foreground elements
# Color used for indicating danger or loss (e.g., health bar)
RED = (250, 0, 0)
GREEN = (0, 255, 0)      # Color for positive indicators (e.g., health bar)
BLACK = (0, 0, 0)        # Background color

# Game frame rate
FPS = 90  # Defines the frame rate of the game

# Screen dimensions
SCREEN_WIDTH = 600  # Width of the game window in pixels
SCREEN_HEIGHT = 800  # Height of the game window in pixels

# Enemy configuration
ROW_OF_ENEMIES = 5       # Number of rows of enemy aliens
COLUMN_OF_ENEMIES = 5    # Number of columns of enemy aliens

# Player settings
PLAYER_COOLDOWN = 300        # Cooldown time for player's shooting in milliseconds
PLAYER_START_HEALTH = 3      # Initial health of the player
PLAYER_SPEED = 5             # Speed at which the player's spaceship moves
PLAYER_BULLET_SPEED = 5      # Speed of the bullets shot by the player

# Enemy settings
ENEMY_BULLET_SPEED = 4   # Speed of the bullets shot by the enemies
ALIEN_COOLDOWN = 1000    # Cooldown time for alien's shooting in milliseconds

# Explosion settings
EXPLOSION_SPEED = 3  # Speed of the explosion animations

# Game start countdown
GAME_COOLDOWN = 5   # Countdown before the start of the game
