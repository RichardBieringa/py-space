import pygame

from typing import Protocol, Sequence


class GameObject(Protocol):
    def update(self, key_events: Sequence[bool], canvas: pygame.Surface):
        """Update the game object."""
        ...

    def paint(self, canvas: pygame.Surface):
        """Paint the game object."""
        ...

    def alive(self) -> bool:
        """Checks if the object is in any sprite group."""
        ...
