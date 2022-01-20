from xmlrpc.client import Boolean
import pygame
from typing import Sequence


class Rocket(pygame.sprite.Sprite):
    """A rocket fired by the player."""

    def __init__(self, x_pos, y_pos):
        super().__init__()

        self.rect = pygame.rect.Rect(x_pos, y_pos, 5, 5)
        self.velocity = 5

    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        """Updates the rocket traversing the map."""

        # Move the rocket
        self.rect.move_ip(0, -self.velocity)

        # Check out of bounds
        if self.rect.bottom < canvas.get_rect().top:
            # print(
            #     f"Rocket - top:{self.rect.top}, bottom: {self.rect.bottom}, left: {self.rect.left}, right: {self.rect.right}"
            # )
            self.kill()

    def paint(self, canvas: pygame.Surface):
        """Paint the Rocket on the surface"""

        pygame.draw.circle(canvas, "red", (self.rect.left, self.rect.top), 5)
