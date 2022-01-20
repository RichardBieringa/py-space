import pygame

from typing import Sequence

from py_space.game_objects import ASSETS_DIRECTORY

IMAGE_DIR = ASSETS_DIRECTORY / "ship_red.png"


class Enemy(pygame.sprite.Sprite):
    """Represents an enemy ship"""

    def __init__(
        self, x_pos: int, y_pos: int, width: int = 50, height: int = 40
    ) -> None:
        super().__init__()

        # Loads the image from the assets directory
        image = pygame.image.load(str(IMAGE_DIR))
        # Scale the image
        image = pygame.transform.scale(image, (width, height))
        # Flip the image vertically
        image = pygame.transform.flip(image, 0, 180)

        self.velocity = 1

        self.surface = image
        self.rect = self.surface.get_rect(center=(x_pos, y_pos))

    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        """Update the Enemy ship's position and check if it reaches the bottom."""

        self.rect.move_ip(0, self.velocity)

        # Check out of bounds
        if self.rect.bottom < canvas.get_rect().top:
            self.kill()

    def paint(self, canvas: pygame.Surface):
        """Paint the Enemy on the parent Surface."""

        canvas.blit(self.surface, self.rect)
