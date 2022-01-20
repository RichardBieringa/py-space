from re import X
import py
import pygame

from typing import Sequence

from py_space.game_objects import ASSETS_DIRECTORY

IMAGE_DIR = ASSETS_DIRECTORY / "background.png"


class Background(pygame.sprite.Sprite):
    """Represents an enemy ship"""

    def __init__(self, width: int = 50, height: int = 40) -> None:
        super().__init__()

        # Loads the image from the assets directory
        image = pygame.image.load(str(IMAGE_DIR))

        # Scale the image
        image = pygame.transform.scale(image, (width, height))

        self.surface = image
        self.rect = self.surface.get_rect()

    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        pass

    def paint(self, canvas: pygame.Surface):
        """Renders the background on the surface."""
        canvas.blit(self.surface, self.rect)
