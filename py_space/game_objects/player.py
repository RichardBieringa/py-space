from re import X
import pygame

from typing import Sequence

from py_space.game_objects import ASSETS_DIRECTORY

IMAGE_DIR = ASSETS_DIRECTORY / "ship_yellow.png"


class Player(pygame.sprite.Sprite):
    """Represents a ship (the player)"""

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

        # The speed/velocity of the object
        self.velocity = 5

        self.surface = image
        self.rect = self.surface.get_rect(center=(x_pos, y_pos))

    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        """Update the position of the player ship."""

        # Process player input to handle ship movement
        if key_events[pygame.K_w]:
            self.rect.move_ip(0, -self.velocity)
        if key_events[pygame.K_s]:
            self.rect.move_ip(0, self.velocity)
        if key_events[pygame.K_a]:
            self.rect.move_ip(-self.velocity, 0)
        if key_events[pygame.K_d]:
            self.rect.move_ip(self.velocity, 0)

        # Keep ship on the screen
        parent = canvas.get_rect()
        if self.rect.top < parent.top:
            self.rect.top = parent.top
        if self.rect.bottom > parent.bottom:
            self.rect.bottom = parent.bottom
        if self.rect.left < parent.left:
            self.rect.left = parent.left
        if self.rect.right > parent.right:
            self.rect.right = parent.right

    def paint(self, canvas: pygame.Surface):
        """Paint the Player Ship on the surface"""

        canvas.blit(self.surface, self.rect)
