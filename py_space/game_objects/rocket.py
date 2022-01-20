import pygame
from typing import Sequence


class Rocket(pygame.sprite.Sprite):
    """A rocket fired by the player."""

    def __init__(self, x_pos: int, y_pos: int, width: int = 5, height: int = 5):
        self.x = x_pos
        self.y = y_pos

        self.velocity = 10
        # self.rect = pygame.draw.circle(canvas, "red", (x_pos, y_pos), 10)
        self.rect = pygame.rect(x_pos, y_pos, width, height)

    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        """Updates the rocket traversing the map."""

        # Move the rocket
        self.rect.move_ip(0, -self.velocity)

        # Check out of bounds
        if self.rect.bottom < canvas.get_rect().bottom:
            self.kill()

    def paint(self, canvas: pygame.Surface):
        """Paint the Rocket on the surface"""

        pygame.draw.circle(canvas, "red", (self.rect.left, self.rect.top), 50)
        # canvas.blit(self.surface, self.rect)
