import pygame
from typing import Protocol

class GameObject(Protocol):
    def update(self):
        """Update the game object."""

    def paint(self, canvas: pygame.Surface):
        """Paint the game object."""
