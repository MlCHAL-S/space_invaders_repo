"""
Space Invaders Game Implementation using Pygame

This script is an implementation of the classic arcade game 'Space Invaders' using the Pygame library. The game features a spaceship controlled by the player, whose objective is to defeat waves of incoming alien enemies by shooting them while avoiding their attacks. The game ends when the player either destroys all aliens or loses all health from alien attacks.

Key Features:
- Player-controlled spaceship with movement and shooting capabilities.
- Alien enemies with simple AI for movement and attacking the player.
- Collision detection for bullets impacting aliens and the player's spaceship.
- Explosions animations for visual feedback upon destruction of aliens or the player's spaceship.
- Countdown before the game starts and display messages for game over conditions.
- Background music and sound effects for a more immersive gaming experience.

Classes:
- Spaceship: Manages the player's spaceship, including its movement, shooting, and health.
- Bullet: Handles the bullets fired by the spaceship, their movement, and collision with aliens.
- Alien: Represents the alien enemies with their own movement patterns and shooting behavior.
- AlienBullet: Similar to Bullet, but represents bullets fired by aliens.
- Explosion: Manages explosion animations triggered by collisions.
- SpaceInvadersGame: The main game class that initializes the game, manages game states, and contains the main game loop.

This script exemplifies object-oriented programming in Python and demonstrates the use of the Pygame library for 2D game development.

Usage:
Player can control the spaceship using keyboard inputs and aim to destroy all alien enemies.

Dependencies:
- pygame: A popular Python library for writing video games.

"""
from . import constants
import pygame
from pygame import mixer
from random import choice
import os
mixer.init()


class Spaceship(pygame.sprite.Sprite):
    """
    Represents a spaceship in the Space Invaders game.

    This class manages the behavior and parameters of the player's spaceship, 
    including movement, shooting, health management, and collision detection.

    Parameters:
    -----------
    image : pygame.Surface
        The image of the spaceship.
    rect : pygame.Rect
        The rectangular bounding box of the spaceship.
    health_start : int
        The initial health of the spaceship.
    health_remaining : int
        The current health of the spaceship.
    last_shot : int
        The timestamp of the last shot fired from the spaceship.
    screen : pygame.Surface
        The game screen surface.
    bullet_group : pygame.sprite.Group
        Group containing bullets.
    alien_group : pygame.sprite.Group
        Group containing aliens.
    explosion_group : pygame.sprite.Group
        Group containing explosions.
    explosion_created : bool
        Flag indicating if an explosion has been created.

    Methods:
    --------
    __init__(self, x, y, health, screen, bullet_group, alien_group, explosion_group)
        Initialize the spaceship with position, health, and related groups.
    _move(self)
        Move the spaceship based on user input.
    _shoot(self)
        Shoot a bullet from the spaceship and handle the explosion animation.
    _play_sound(self, sound)
        Play a sound effect.
    _update_mask(self)
        Update the mask for collision detection.
    _update_health_bar(self)
        Update the health bar of the spaceship.
    update(self)
        Update the spaceship's position, shooting, mask, health, and health bar.

    """

    def __init__(
        self,
        x: int,
        y: int,
        health: int,
        screen: pygame.Surface,
        bullet_group: pygame.sprite.Group,
        alien_group: pygame.sprite.Group,
        explosion_group: pygame.sprite.Group,
    ) -> None:
        """
        Initialize the spaceship.

        Args:
            x (int): The x-coordinate of the spaceship's initial position.
            y (int): The y-coordinate of the spaceship's initial position.
            health (int): The initial health of the spaceship.
            screen (pygame.Surface): The game screen surface.
            bullet_group (pygame.sprite.Group): Group containing bullets.
            alien_group (pygame.sprite.Group): Group containing aliens.
            explosion_group (pygame.sprite.Group): Group containing explosions.
        """
        pygame.sprite.Sprite.__init__(self)

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(
            current_dir, 'player_sprites', 'spaceship.png')

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

        self.rect.center = (x, y)
        self.health_start = constants.PLAYER_START_HEALTH
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()
        self.screen = screen
        self.bullet_group = bullet_group
        self.alien_group = alien_group
        self.explosion_group = explosion_group
        self.explosion_created = False

    def _move(self) -> None:
        """
        Move the spaceship based on user input.
        """
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= constants.PLAYER_SPEED
        if key[pygame.K_RIGHT] and self.rect.right < constants.SCREEN_WIDTH:
            self.rect.x += constants.PLAYER_SPEED

    def _shoot(self) -> None:
        """
        Shoot a bullet from the spaceship and handle the explosion animation.
        """
        key = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        if key[pygame.K_SPACE] and (time_now - self.last_shot > constants.PLAYER_COOLDOWN) and self.health_remaining > 0:
            bullet = Bullet(
                self.rect.centerx, self.rect.top, self.alien_group, self.explosion_group
            )
            self._play_sound('sounds/player_shot.wav')
            self.bullet_group.add(bullet)
            self.last_shot = time_now

    def _play_sound(self, sound: str) -> None:
        """
        Play a sound effect.

        Args:
            sound (str): The path to the sound file.
        """
        current_dir = os.path.dirname(__file__)
        sound_path = os.path.join(current_dir, sound)

        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(0.5)
        sound.play()

    def _update_mask(self) -> None:
        """
        Update the mask for collision detection.
        """
        self.mask = pygame.mask.from_surface(self.image)

    def _update_health_bar(self) -> None:
        """
        Update the health bar of the spaceship.
        """
        if self.health_remaining > 0:
            pygame.draw.rect(
                self.screen,
                constants.RED,
                (self.rect.x, self.rect.bottom + 10, self.rect.width, 15),
            )
            pygame.draw.rect(
                self.screen,
                constants.GREEN,
                (
                    self.rect.x,
                    self.rect.bottom + 10,
                    int(self.rect.width * (self.health_remaining / self.health_start)),
                    15,
                ),
            )
        elif self.health_remaining <= 0:
            # Create an explosion at the center of the spaceship only once
            if not self.explosion_created:
                explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
                self.explosion_group.add(explosion)
                self.explosion_created = True
            self.kill()

    def update(self) -> None:
        """
        Update the spaceship's position, shooting, mask, health, and health bar.
        """
        self._move()
        self._shoot()
        self._update_mask()
        self._update_health_bar()


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the player's spaceship.

    Parameters:
        image (pygame.Surface): The image of the bullet.
        rect (pygame.Rect): The rectangular bounding box of the bullet.
        alien_group (pygame.sprite.Group): Group containing aliens.
        explosion_group (pygame.sprite.Group): Group containing explosions.

    Methods:
        __init__(self, x: int, y: int, alien_group: pygame.sprite.Group, explosion_group: pygame.sprite.Group) -> None:
            Initialize a bullet.

        _movement(self) -> None:
            Move the bullet upward.

        _collision(self) -> None:
            Check for collision with aliens and handle collisions.

        update(self) -> None:
            Update the bullet's movement and collision detection.
    """

    def __init__(
        self,
        x: int,
        y: int,
        alien_group: pygame.sprite.Group,
        explosion_group: pygame.sprite.Group,
    ) -> None:
        """
        Initialize a bullet.

        Args:
            x (int): The x-coordinate of the bullet's initial position.
            y (int): The y-coordinate of the bullet's initial position.
            alien_group (pygame.sprite.Group): Group containing aliens.
            explosion_group (pygame.sprite.Group): Group containing explosions.
        """
        pygame.sprite.Sprite.__init__(self)

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(
            current_dir, 'player_sprites', 'player_bullet.png')

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alien_group = alien_group
        self.explosion_group = explosion_group

    def _movement(self) -> None:
        """
        Move the bullet upward.
        """
        self.rect.y -= constants.PLAYER_BULLET_SPEED
        if self.rect.y < -10:
            self.kill()

    def _collision(self) -> None:
        """
        Check for collision with aliens and handle collisions.
        """
        if pygame.sprite.spritecollide(self, self.alien_group, True):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            self.explosion_group.add(explosion)

    def update(self) -> None:
        """
        Update method for the Bullet class.
        """
        self._movement()
        self._collision()


class Alien(pygame.sprite.Sprite):
    """
    Represents an alien enemy in the game.

    Parameters:
        image (pygame.Surface): The image of the alien.
        rect (pygame.Rect): The rectangular bounding box of the alien.
        move_counter (int): Counter for movement to control direction change.
        move_direction (int): Direction of alien movement (1 for right, -1 for left).

    Methods:
        __init__(self, x: int, y: int) -> None:
            Initialize an alien.

        _movement(self) -> None:
            Move the alien horizontally with periodic direction change.

        update(self) -> None:
            Update the alien's movement.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize an alien.

        Args:
            x (int): The x-coordinate of the alien's initial position.
            y (int): The y-coordinate of the alien's initial position.
        """
        pygame.sprite.Sprite.__init__(self)

        current_dir = os.path.dirname(__file__)
        random_choice = choice([1, 2, 3])
        image_path = os.path.join(
            current_dir, 'enemy_sprites', f'enemy{random_choice}.png')

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_counter = 0
        self.move_direction = 1

    def _movement(self) -> None:
        """
        Move the alien horizontally with periodic direction change.
        """
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

    def update(self) -> None:
        """
        Update method for the Alien class.
        :noindex:
        """
        self._movement()


class AlienBullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by an alien enemy.

    Parameters:
        image (pygame.Surface): The image of the alien bullet.
        rect (pygame.Rect): The rectangular bounding box of the alien bullet.
        spaceship_group (pygame.sprite.Group): Group containing the player's spaceship.
        explosion_group (pygame.sprite.Group): Group containing explosions.
    """

    def __init__(
        self,
        x: int,
        y: int,
        spaceship_group: pygame.sprite.Group,
        explosion_group: pygame.sprite.Group,
    ) -> None:
        """
        Initialize an alien bullet.

        Args:
            x (int): The x-coordinate of the bullet's initial position.
            y (int): The y-coordinate of the bullet's initial position.
            spaceship_group (pygame.sprite.Group): Group containing the player's spaceship.
            explosion_group (pygame.sprite.Group): Group containing explosions.
        """
        pygame.sprite.Sprite.__init__(self)

        current_dir = os.path.dirname(__file__)
        image_path = os.path.join(
            current_dir, 'enemy_sprites', 'enemy_bullet.png')

        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spaceship_group = spaceship_group
        self.explosion_group = explosion_group

    def _movement(self) -> None:
        """
        Move the alien bullet downward.
        """
        self.rect.y += constants.ENEMY_BULLET_SPEED
        if self.rect.bottom > constants.SCREEN_HEIGHT + 10:
            self.kill()

    def _collision(self) -> None:
        """
        Check for collision with the spaceship and handle collisions.
        """
        if pygame.sprite.spritecollide(
            self, self.spaceship_group, False, pygame.sprite.collide_mask
        ):
            self.kill()
            spaceship = self.spaceship_group.sprites()[0]
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            self.explosion_group.add(explosion)

    def update(self) -> None:
        """
        Update the alien bullet's movement and collision detection.
        """
        self._movement()
        self._collision()


class Explosion(pygame.sprite.Sprite):
    """
    Represents an explosion animation in the game.

    Parameters:
        images (list): List of explosion animation frames.
        index (int): Current frame index of the explosion animation.
        image (pygame.Surface): The current frame image.
        rect (pygame.Rect): The rectangular bounding box of the explosion animation.
        counter (int): Counter for frame update timing.
        sound (pygame.mixer.Sound): The sound effect associated with the explosion.

    Methods:
        __init__(self, x: int, y: int, size: int) -> None:
            Initialize an explosion animation.

        update(self) -> None:
            Update the explosion animation.
    """

    def __init__(self, x: int, y: int, size: int) -> None:
        """
        Initialize an explosion animation.

        Args:
            x (int): The x-coordinate of the explosion's center.
            y (int): The y-coordinate of the explosion's center.
            size (int): The size of the explosion (1, 2, or 3).
        """
        pygame.sprite.Sprite.__init__(self)

        current_dir = os.path.dirname(__file__)

        self.images = list()
        for num in range(1, 6):
            image_path = os.path.join(current_dir, 'effects', f'exp{num}.png')
            img = pygame.image.load(image_path)

            # Scale the image based on the 'size' parameter
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            elif size == 2:
                img = pygame.transform.scale(img, (40, 40))
            elif size == 3:
                img = pygame.transform.scale(img, (100, 100))

            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

        current_dir = os.path.dirname(__file__)
        path = os.path.join(current_dir, 'sounds', 'explosion.wav')
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(0.5)
        self.sound.play()

    def update(self) -> None:
        """
        Update the Explosion class.
        """
        self.counter += 1

        if (
            self.counter >= constants.EXPLOSION_SPEED
            and self.index < len(self.images) - 1
        ):
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if (
            self.index >= len(self.images) - 1
            and self.counter >= constants.EXPLOSION_SPEED
        ):
            self.kill()


class SpaceInvadersGame:
    """
    Represents the state and main game logic for Space Invaders.

    Parameters:
        screen (pygame.Surface): The game display surface.
        clock (pygame.time.Clock): The game clock for controlling frame rate.
        countdown (int): Countdown timer at the start of the game.
        last_count (int): Timestamp for the last countdown update.
        last_alien_shot (int): Timestamp for the last alien shot.
        spaceship_group (pygame.sprite.GroupSingle): Group containing the player's spaceship.
        bullet_group (pygame.sprite.Group): Group containing player bullets.
        alien_group (pygame.sprite.Group): Group containing alien enemies.
        alien_bullet_group (pygame.sprite.Group): Group containing alien bullets.
        explosion_group (pygame.sprite.Group): Group containing explosion animations.
        spaceship (Spaceship): The player's spaceship.
        game_over (int): Flag indicating the game's state (0 for ongoing, 1 for win, -1 for loss).
        end_timer (int): Timestamp for the game ending timer.
        ending_music (bool): Flag to control ending music playback.
    """

    def __init__(self) -> None:
        """
        Initialize the Space Invaders game.
        """
        # Initialize display
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        current_dir = os.path.dirname(__file__)

        # Load the image
        image_path = os.path.join(current_dir, 'effects', 'background.png')
        self.BACKGROUND = pygame.image.load(image_path)

        # Loading fonts
        image_path = os.path.join(current_dir, 'fonts', 'font.ttf')
        self.FONT_40 = pygame.font.Font(image_path, 40)

        # Game variables
        self.countdown = constants.GAME_COOLDOWN
        self.game_over = 0
        self.end_timer = 0
        self.last_count = pygame.time.get_ticks()
        self.last_alien_shot = pygame.time.get_ticks()
        self.ending_music = True

        # Create sprite groups
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.bullet_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()

        # Create player
        self.spaceship = Spaceship(
            int(constants.SCREEN_WIDTH / 2),
            int(constants.SCREEN_HEIGHT * 4 / 5),
            3,
            self.screen,
            self.bullet_group,
            self.alien_group,
            self.explosion_group,
        )

        # Add spaceship to group
        self.spaceship_group.add(self.spaceship)

        # Spawn enemies
        self._spawn_aliens()

        # start main music
        self._play_sound('sounds/background_music.wav')

    def _spawn_aliens(self):
        """
        Spawn the initial alien enemies.
        """
        for row in range(constants.ROW_OF_ENEMIES):
            for item in range(constants.COLUMN_OF_ENEMIES):
                alien = Alien(100 + item * 100, 100 + row * 70)
                self.alien_group.add(alien)

    def _draw_bg(self):
        """
        Draw the game background.
        """

        self.screen.blit(self.BACKGROUND, (0, 0))

    def _draw_text(self, text, font, text_col, x, y):
        """
        Draw text on the game screen.

        Args:
            text (str): The text to display.
            font (pygame.font.Font): The font to use for the text.
            text_col (tuple): The color of the text.
            x (int): The x-coordinate of the text.
            y (int): The y-coordinate of the text.
        """
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def _play_sound(self, sound):
        # Construct the relative path to the sound file
        current_dir = os.path.dirname(__file__)
        sound_path = os.path.join(current_dir, sound)

        # Load and play the sound
        sound_temp = pygame.mixer.Sound(sound_path)
        sound_temp.set_volume(0.5)
        sound_temp.play()

    def play_step(self):
        """
        Execute a single game step.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        # Display background
        self._draw_bg()

        self.spaceship_group.draw(self.screen)
        self.bullet_group.draw(self.screen)
        self.alien_group.draw(self.screen)
        self.alien_bullet_group.draw(self.screen)
        self.explosion_group.draw(self.screen)

        self.explosion_group.update()

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if self.countdown == 0:
            aliens_left = len(self.alien_group)

            # Update spaceship and game elements
            self.spaceship.update()
            self.bullet_group.update()
            self.alien_group.update()
            self.alien_bullet_group.update()

            # Alien's shooting
            time_now = pygame.time.get_ticks()
            if aliens_left and self.spaceship.health_remaining and (time_now - self.last_alien_shot > constants.ALIEN_COOLDOWN):
                attacking_alien = choice(self.alien_group.sprites())
                alien_bullet = AlienBullet(
                    attacking_alien.rect.centerx,
                    attacking_alien.rect.bottom,
                    self.spaceship_group,
                    self.explosion_group,
                )
                self._play_sound('sounds/enemy_shot.wav')
                self.alien_bullet_group.add(alien_bullet)
                self.last_alien_shot = time_now
            else:
                # Ending the game if all enemies are dead
                if aliens_left == 0:
                    if self.ending_music:
                        self._play_sound('sounds/win.wav')
                        self.ending_music = False

                    self._draw_text(
                        "YOU WIN!",
                        self.FONT_40,
                        constants.WHITE,
                        int(constants.SCREEN_WIDTH / 2 - 110),
                        int(constants.SCREEN_HEIGHT / 2 + 50),
                    )

                if self.spaceship.health_remaining == 0:
                    if self.ending_music:
                        self._play_sound('sounds/loss.wav')
                        self.ending_music = False

                    self._draw_text(
                        "GAME OVER!",
                        self.FONT_40,
                        constants.WHITE,
                        int(constants.SCREEN_WIDTH / 2 - 110),
                        int(constants.SCREEN_HEIGHT / 2 + 50),
                    )
                pygame.display.update()
                if pygame.time.get_ticks() - self.end_timer > 3000:
                    return True
                else:
                    return False
        else:
            self._draw_text(
                "GET READY!",
                self.FONT_40,
                constants.WHITE,
                int(constants.SCREEN_WIDTH / 2 - 110),
                int(constants.SCREEN_HEIGHT / 2 + 50),
            )
            self._draw_text(
                str(self.countdown),
                self.FONT_40,
                constants.WHITE,
                int(constants.SCREEN_WIDTH / 2 - 10),
                int(constants.SCREEN_HEIGHT / 2 + 100),
            )
            count_timer = pygame.time.get_ticks()
            if count_timer - self.last_count > 1000:
                self.countdown -= 1
                self.last_count = count_timer

        self.end_timer = pygame.time.get_ticks()
        pygame.display.update()
        self.clock.tick(constants.FPS)

        return False
