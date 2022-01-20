import pygame

from typing import Sequence

from py_space.game_objects import ASSETS_DIRECTORY

IMAGE_DIR = ASSETS_DIRECTORY / "ship_yellow.png"


class Player(pygame.sprite.Sprite):
    """Represents a ship (the player)"""

    def __init__(
        self, canvas: pygame.Surface, width: int = 50, height: int = 40
    ) -> None:
        super().__init__()

        # Loads the image from the assets directory
        image = pygame.image.load(str(IMAGE_DIR))

        # Scale the image
        image = pygame.transform.scale(image, (width, height))

        # Flip the image vertically
        image = pygame.transform.flip(image, 0, 180)

        # The parent canvas on which this will be painted
        self.canvas = canvas
        self.parent_rect = self.canvas.get_rect()

        # The speed/velocity of the object
        self.speed = 5

        self.surface = image
        self.rect = self.surface.get_rect(
            center=(
                (self.parent_rect.right - self.parent_rect.left) / 2,
                self.parent_rect.bottom + 50,
            )
        )

    def update(self, pressed_keys: Sequence[bool]):
        """Updates the position of the ship."""

        if pressed_keys[pygame.K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[pygame.K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_d]:
            self.rect.move_ip(self.speed, 0)

        # Keep ship on the screen
        parent = self.canvas.get_rect()

        if self.rect.top < parent.top:
            self.rect.top = parent.top
        if self.rect.bottom > parent.bottom:
            self.rect.bottom = parent.bottom
        if self.rect.left < parent.left:
            self.rect.left = parent.left
        if self.rect.right > parent.right:
            self.rect.right = parent.right

    def paint(self):
        """Paint the Game Object on the surface"""
        self.canvas.blit(self.surface, self.rect)
