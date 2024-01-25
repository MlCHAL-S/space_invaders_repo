"""
Space Invaders Game Package
----------------------------

This package contains the implementation of a Space Invaders-style game using Pygame. 
It is structured into modular components, each handling different aspects of the game's functionality. 
The package is designed with object-oriented principles, allowing for clear separation of concerns and 
ease of future enhancements.

Modules:
--------

- constants
    Defines all the constants used throughout the game, including screen dimensions, 
    color definitions, gameplay settings, and more.

- classes
    Contains the classes that represent the different entities in the game such as the player's spaceship, 
    aliens, bullets, and explosions. It also includes the main game class that orchestrates the game loop and logic.

Usage:
------

To run the game, ensure that Pygame is installed and execute the main game script.

"""
from .classes import SpaceInvadersGame, Spaceship, Explosion, Alien, AlienBullet, Bullet
from .constants import *
