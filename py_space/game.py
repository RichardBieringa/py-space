import logging
import sys

from typing import Sequence, List

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

        # Creates the player ship
        self.player = player.Player(self.screen)
        self.add_game_object(self.player)

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

    def add_game_object(self, game_object: game_object_proto.GameObject) -> None:
        """Adds a game object to the game."""
        self.objects.append(game_object)

    def remove_game_object(self, game_object: game_object_proto.GameObject) -> None:
        """Remove a game object to the game."""
        self.objects.remove(game_object)

    def handle_player_input(self, pressed_keys: Sequence[bool]):

        if pressed_keys[pygame.K_SPACE]:
            self.objects.append(pygame)

        pass

    def _draw_game_objects(self) -> None:
        """Updates the location of all game objects and draws them on the screen"""

        # Other updates updates
        for object in self.objects:
            object.update()
            object.paint(self.screen)

    def _run(self):

        # test_surface = pygame.Surface((100, 200))
        # test_surface.fill("red")

        # test_font = pygame.font.Font(None, 50)
        # text_surface = test_font.render("My Game", False, "GREEN")

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    logging.info("Quiting the game...")
                    self.quit_game()

            keys_pressed = pygame.key.get_pressed()

            pygame.display.update()

            # Make it black
            self.screen.fill((0, 0, 0))

            self.clock.tick(self.fps)
