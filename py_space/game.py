import logging
import sys
import random
from typing import Sequence, List, Optional

import pygame

from py_space.game_objects import proto
from py_space.game_objects import background
from py_space.game_objects import player
from py_space.game_objects import enemy
from py_space.game_objects import rocket


class Game:
    """Represents the python space adventure game"""

    def __init__(
        self, title: str, fps: int = 60, width: int = 900, height: int = 800
    ) -> None:
        pygame.init()

        # Generic Configuration
        self.title = title
        self.fps = fps
        self.screen_height = height
        self.screen_width = width
        self.running = False
        self.clock = pygame.time.Clock()
        self.objects: List[proto.GameObject] = []

        # Creates the screen on which the game is drawn
        self.screen = pygame.display.set_mode((width, height))

        # Sets the window title of the screen
        pygame.display.set_caption(self.title)

        self.initialize_space_game()

    def initialize_space_game(self):
        """Sets up the game specific details."""

        self.enemies = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # Places the player in the middle above the bottom of the screen
        screen_rect = self.screen.get_rect()
        player_x = (screen_rect.right - screen_rect.left) / 2
        player_y = (screen_rect.bottom) + 20

        # Adds a background image to the game objects
        self.background = background.Background(self.screen_width, self.screen_height)
        self.add_game_object(self.background)

        # Inserts the player into the game
        self.player = player.Player(player_x, player_y)
        self.add_game_object(self.player)

        self.last_bullet = 0

    def run_game(self) -> None:
        """Starts the game"""
        self.running = True

        self._run()

    def stop_game(self) -> None:
        """Stops/Pauses the game"""
        self.running = False

    def quit_game(self) -> None:
        """Quits the game and unloads pygame."""

        self.stop_game()
        pygame.quit()
        sys.exit()

    def add_game_object(
        self,
        game_object: proto.GameObject,
        sprite_group: Optional[Sequence[pygame.sprite.Sprite]] = None,
    ) -> None:
        """Adds a game object to the game and to a sprite group if provided."""

        self.objects.append(game_object)
        self.all_sprites.add(game_object)

        # Add to custom sprite group if supplied
        if sprite_group is not None:
            sprite_group.add(game_object)

    def remove_game_object(self, game_object: proto.GameObject) -> None:
        """Remove a game object to the game."""
        self.objects.remove(game_object)

    def _update_game_objects(self, key_events: Sequence[bool]) -> None:
        """Updates the location of all game objects and draws them on the screen."""

        # Other updates updates
        for object in self.objects:
            object.update(key_events, self.screen)
            object.paint(self.screen)

            # Check if the object is dead/not relevant to clean up
            if not object.alive():
                self.objects.remove(object)

    def _fire_rocket(self) -> bool:
        """Lets the player fire a rocket.

        Checks if there are less than 4 rockets in the game, and prevents spamming
        by introducing a delay between rockets.

        Returns True on succesful fire, else False"""

        # Can't have more than 4 rockets in the game
        if len(self.rockets) > 4:
            logging.info(
                "Fire Rocket (false) - Too many rockets %s",
                len(self.rockets),
            )
            return False

        # Prevent 'spamming' rockets due to the key being held (300 ms delay)
        now = pygame.time.get_ticks()
        time_since_last_bullet = now - self.last_bullet

        if time_since_last_bullet < 300:
            logging.info("Fire Rocket (false) - Can't fire that fast in succession")
            return False

        # Gets the position for the rocket to spawn
        player_rect = self.player.rect
        x_pos = player_rect.centerx
        y_pos = player_rect.top + 5

        rocket_instance = rocket.Rocket(x_pos, y_pos)
        self.add_game_object(rocket_instance, self.rockets)

        self.last_bullet = now

        logging.info("Fire Rocket (True)")

        return True

    def _spawn_enemy(self):
        """Spawns a enemy on the field."""

        # Get a random location somewhwere above the playable surface
        screen_rect = self.screen.get_rect()
        x_pos = random.randint(screen_rect.left + 10, screen_rect.right - 10)
        y_pos = random.randint(screen_rect.top + 10, screen_rect.top + 50)

        enemy_instance = enemy.Enemy(x_pos, y_pos)
        self.add_game_object(enemy_instance, self.enemies)

    def _run(self):
        """Runs the main game loop."""

        # Create a custom event for adding a new enemy
        SPAWN_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(SPAWN_ENEMY, 400)

        while self.running:

            # Set the screen black
            self.screen.fill((0, 0, 0))

            # Get all pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logging.info("Quiting the game...")
                    self.quit_game()

                if event.type == SPAWN_ENEMY:
                    logging.info("Spawning an enemy...")
                    self._spawn_enemy()

            # Get a list of which keys are pressed by the user
            key_events = pygame.key.get_pressed()

            # Fire a rocket above the player
            if key_events[pygame.K_SPACE]:
                self._fire_rocket()

            # Updates all the game objects and draws them on screen
            self._update_game_objects(key_events)

            # Check if a rocket killed any enemy
            if pygame.sprite.groupcollide(self.rockets, self.enemies, True, True):
                print("pew pew")

            # The player collides with an enemy and loses the game
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                print("You are dead, game over...")
                self.player.kill()
                self.stop_game()

            pygame.display.update()
