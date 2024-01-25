"""
Unit Tests for Space Invaders Game Classes

This file contains a series of unit tests for the various classes used in the Space Invaders game.
These tests ensure that each class is correctly initialized and performs its intended functions.

The following classes are tested in this file:
- Spaceship: Tests its initialization and attributes.
- Bullet: Tests its initialization and attributes.
- Alien: Tests its initialization and attributes.
- AlienBullet: Tests its initialization and attributes.
- Explosion: Tests its initialization and attributes.
- SpaceInvadersGame: Tests the game initialization and attributes.

Each test case within this file focuses on specific aspects of these classes, including attribute initialization,
functional behavior, and correctness.

"""
import unittest
import pygame
from unittest.mock import patch
import sys
import os

test_dir = os.path.dirname(__file__)
project_root = os.path.dirname(test_dir)
sys.path.append(project_root)

from src.space_invaders_package.source import constants
from src.space_invaders_package.source import Spaceship, Bullet, Alien, AlienBullet, Explosion, SpaceInvadersGame

class TestSpaceship(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def test_initialization(self):
        screen = pygame.Surface((800, 600))
        bullet_group = pygame.sprite.Group()
        alien_group = pygame.sprite.Group()
        explosion_group = pygame.sprite.Group()

        # Create an instance of the Spaceship class
        spaceship = Spaceship(100, 200, 3, screen,
                              bullet_group, alien_group, explosion_group)

        # Check if attributes are initialized correctly
        self.assertEqual(spaceship.rect.center, (100, 200))
        self.assertEqual(spaceship.health_remaining, 3)
        self.assertEqual(spaceship.health_start, constants.PLAYER_START_HEALTH)
        # Add more assertions based on your class attributes

        # Check if pygame.sprite.Sprite.__init__ is called
        self.assertTrue(isinstance(spaceship, pygame.sprite.Sprite))

        # Check if the image and rect attributes are initialized
        self.assertIsInstance(spaceship.image, pygame.Surface)
        self.assertIsInstance(spaceship.rect, pygame.Rect)

        # Check if the last_shot attribute is initialized to the current time
        self.assertEqual(spaceship.last_shot, pygame.time.get_ticks())

        # Check if other attributes are initialized correctly
        self.assertIs(spaceship.screen, screen)
        self.assertIs(spaceship.bullet_group, bullet_group)
        self.assertIs(spaceship.alien_group, alien_group)
        self.assertIs(spaceship.explosion_group, explosion_group)

    def tertDown(self):
        pygame.quit()


class TestBullet(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources or dependencies for the tests.
        pygame.init()

    def tearDown(self):
        # Clean up any resources used during testing.
        pygame.quit()

    def test_initialization(self):
        # Create test data
        x = 100
        y = 200
        alien_group = pygame.sprite.Group()
        explosion_group = pygame.sprite.Group()

        # Initialize the bullet
        bullet = Bullet(x, y, alien_group, explosion_group)

        # Perform assertions to check if the initialization is correct
        self.assertIsInstance(bullet, pygame.sprite.Sprite)
        self.assertEqual(bullet.rect.center, (x, y))
        self.assertEqual(bullet.alien_group, alien_group)
        self.assertEqual(bullet.explosion_group, explosion_group)


class TestAlien(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources or dependencies for the tests.
        pygame.init()

    def tearDown(self):
        # Clean up any resources used during testing.
        pygame.quit()

    def test_initialization(self):
        # Create test data
        x = 100
        y = 200

        # Initialize the alien
        alien = Alien(x, y)

        # Perform assertions to check if the initialization is correct
        self.assertIsInstance(alien, pygame.sprite.Sprite)
        self.assertEqual(alien.rect.center, (x, y))
        self.assertEqual(alien.move_counter, 0)
        self.assertEqual(alien.move_direction, 1)


class TestAlienBullet(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources or dependencies for the tests.
        pygame.init()

    def tearDown(self):
        # Clean up any resources used during testing.
        pygame.quit()

    def test_initialization(self):
        # Create test data
        x = 100
        y = 200
        spaceship_group = pygame.sprite.Group()
        explosion_group = pygame.sprite.Group()

        # Initialize the alien bullet
        alien_bullet = AlienBullet(x, y, spaceship_group, explosion_group)

        # Perform assertions to check if the initialization is correct
        self.assertIsInstance(alien_bullet, pygame.sprite.Sprite)
        self.assertEqual(alien_bullet.rect.center, (x, y))
        self.assertEqual(alien_bullet.spaceship_group, spaceship_group)
        self.assertEqual(alien_bullet.explosion_group, explosion_group)


class TestExplosion(unittest.TestCase):
    def setUp(self):
        # Set up any necessary resources or dependencies for the tests.
        pygame.init()

    def tearDown(self):
        # Clean up any resources used during testing.
        pygame.quit()

    def test_init(self):
        # Create a MagicMock for pygame.sprite.Sprite to avoid actual initialization
        with patch.object(pygame.sprite.Sprite, '__init__', return_value=None):
            # Set up inputs for the constructor
            x = 50
            y = 60
            size = 2

            # Create an instance of your class
            explosion = Explosion(x, y, size)

            # Assertions for the initialization
            self.assertEqual(explosion.index, 0)
            self.assertEqual(explosion.counter, 0)

            # Check if the images list is not empty
            self.assertTrue(explosion.images)

            # Check if the image dimensions are correctly scaled based on the size parameter
            for img in explosion.images:
                if size == 1:
                    self.assertEqual(img.get_size(), (20, 20))
                elif size == 2:
                    self.assertEqual(img.get_size(), (40, 40))
                elif size == 3:
                    self.assertEqual(img.get_size(), (100, 100))

            # Check if the rect center is set correctly
            self.assertEqual(explosion.rect.center, (x, y))


class TestSpaceInvadersGame(unittest.TestCase):

    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        game_instance = SpaceInvadersGame()

        # Test that the necessary attributes are initialized
        self.assertIsInstance(game_instance.screen, pygame.Surface)
        self.assertEqual(game_instance.screen.get_size(),
                         (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        self.assertEqual(pygame.display.get_caption()[0], "Space Invaders")
        self.assertIsInstance(game_instance.clock, pygame.time.Clock)
        self.assertEqual(game_instance.countdown, 5)
        self.assertIsInstance(game_instance.last_count, int)
        self.assertIsInstance(game_instance.last_alien_shot, int)
        self.assertEqual(game_instance.game_over, 0)
        self.assertEqual(game_instance.end_timer, 0)

        # Test sprite groups
        self.assertIsInstance(game_instance.spaceship_group,
                              pygame.sprite.GroupSingle)
        self.assertIsInstance(game_instance.bullet_group, pygame.sprite.Group)
        self.assertIsInstance(game_instance.alien_group, pygame.sprite.Group)
        self.assertIsInstance(
            game_instance.alien_bullet_group, pygame.sprite.Group)
        self.assertIsInstance(
            game_instance.explosion_group, pygame.sprite.Group)

        # Test player creation
        self.assertIsInstance(game_instance.spaceship, Spaceship)
        self.assertEqual(game_instance.spaceship.rect.center[0],
                         int(constants.SCREEN_WIDTH / 2))
        self.assertEqual(game_instance.spaceship.rect.center[1],
                         int(constants.SCREEN_HEIGHT * 4 / 5))
        self.assertEqual(game_instance.spaceship.health_start, 3)


if __name__ == '__main__':
    unittest.main()
