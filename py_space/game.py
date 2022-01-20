import logging
from re import S
import sys

from typing import Sequence, List
import py

import pygame

from py_space.game_objects import proto
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
        self.sprites = pygame.sprite.Group()

        # Places the player in the middle above the bottom of the screen
        screen_rect = self.screen.get_rect()
        player_x = (screen_rect.right - screen_rect.left) / 2
        player_y = (screen_rect.bottom) + 20

        # Inserts the player into the game
        self.player = player.Player(player_x, player_y)
        self.add_game_object(self.player)
        self.sprites.add(self.player)

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

    def add_game_object(self, game_object: proto.GameObject) -> None:
        """Adds a game object to the game."""
        self.objects.append(game_object)

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
            logging.log(
                logging.INFO,
                "Fire Rocket (false) - Too many rockets %s",
                len(self.rockets),
            )
            return False

        # Prevent 'spamming' rockets due to the key being held (300 ms delay)
        now = pygame.time.get_ticks()
        time_since_last_bullet = now - self.last_bullet

        if time_since_last_bullet < 300:
            logging.log(
                logging.INFO, "Fire Rocket (false) - Can't fire that fast in succession"
            )
            return False

        # Gets the position for the rocket to spawn
        player_rect = self.player.rect
        x_pos = player_rect.centerx
        y_pos = player_rect.top + 5

        rocket_instance = rocket.Rocket(x_pos, y_pos)
        self.add_game_object(rocket_instance)
        self.rockets.add(rocket_instance)

        self.last_bullet = now

        logging.log(logging.INFO, "Fire Rocket (True)")

        return True

    def _run(self):
        """Runs the main game loop."""

        while self.running:

            # Set the screen black
            self.screen.fill((0, 0, 0))

            # Get all pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    logging.info("Quiting the game...")
                    self.quit_game()

            # Get a list of which keys are pressed by the user
            key_events = pygame.key.get_pressed()

            # Fire a rocket above the player
            if key_events[pygame.K_SPACE]:
                self._fire_rocket()

            # Updates all the game objects and draws them on screen
            self._update_game_objects(key_events)

            pygame.display.update()
