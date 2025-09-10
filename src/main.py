import pygame
from game import Game

def main():
    pygame.init()
    
    # Try to initialize mixer for sound (may fail in WSL or headless environments)
    try:
        pygame.mixer.init()
        print("Audio system initialized successfully")
    except pygame.error as e:
        print(f"Could not initialize audio system: {e}")
        print("Game will run without sound")
    
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
