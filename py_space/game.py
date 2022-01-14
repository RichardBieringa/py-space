import logging
from typing import List, Dict, Tuple

import pygame

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.DEBUG)

WINDOW_SIZE = 900, 500
WINDOW = pygame.display.set_mode(WINDOW_SIZE)


def main() -> None:

    running = True
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                logging.info("Quiting the game...")
                running = False


if __name__ == "__main__":
    main()
