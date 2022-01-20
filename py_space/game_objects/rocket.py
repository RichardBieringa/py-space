import pygame


class Rocket(pygame.sprite.Sprite):
    """A rocket fired by the player."""

    def __init__(self, canvas: pygame.Surface, x_pos: int, y_pos: int, speed: int):
        self.x = x_pos
        self.y = y_pos
        self.velocity = speed

        self.rect = pygame.draw.circle(canvas, "red", (x_pos, y_pos), 10)

    def update(self):
        """Updates the rocket traversing"""

        self.rect.move_ip(0, -self.velocity)

        if self.rect.bottom < 0:
            self.kill()

    def paint(self):
        """Paint the Game Object on the surface"""
        self.canvas.blit(self.surface, self.rect)
