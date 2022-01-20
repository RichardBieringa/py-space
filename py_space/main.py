from py_space import game

GAME_TITLE = "Space Invaders"
GAME_FPS = 60
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800

def main() -> None:
    """Starts the execution of the game."""

    space_invaders = game.Game(GAME_TITLE, GAME_FPS, SCREEN_WIDTH, SCREEN_HEIGHT)
    space_invaders.run_game()

if __name__ == "__main__":
    main()
