import pygame
import random
import config
from utils import load_image, get_random_position
from sprites.zombie import Zombie
from ui import GameUI
from weapon_cursor import WeaponCursor

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Zombie Whacker Game")

        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game states
        self.game_state = "start"  # start, playing, game_over
        
        # Load background (fallback to solid color if not available)
        try:
            self.background = load_image("background/background.jpg", convert_alpha=False)
            self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))  # Dark gray background
        
        # Game objects
        self.zombies = pygame.sprite.Group()
        self.ui = GameUI()
        self.weapon_cursor = WeaponCursor()
        
        # Game variables
        self.score = 0
        self.misses = 0
        self.game_start_time = 0
        self.last_zombie_spawn = 0
        self.last_click_pos = None
        
    def reset_game(self):
        """Reset game for new round"""
        self.zombies.empty()
        self.score = 0
        self.misses = 0
        self.game_start_time = pygame.time.get_ticks()
        self.last_zombie_spawn = 0
        self.game_state = "playing"

    def run(self):
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == "start" or self.game_state == "game_over":
                        self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == "game_over":
                        self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "playing" and event.button == 1:  # Left click
                    self.handle_click(event.pos)
    
    def handle_click(self, pos):
        """Handle mouse click on zombies"""
        self.last_click_pos = pos
        self.weapon_cursor.start_swing_animation()
        
        clicked_zombie = None
        for zombie in self.zombies:
            if zombie.rect.collidepoint(pos) and zombie.alive:
                clicked_zombie = zombie
                break
        
        if clicked_zombie and clicked_zombie.on_click():
            self.score += config.POINTS_PER_HIT
    
    def update(self):
        if self.game_state != "playing":
            return
        
        # Update weapon cursor
        self.weapon_cursor.update()
        
        current_time = pygame.time.get_ticks()
        
        # Check game time
        elapsed_time = (current_time - self.game_start_time) / 1000
        if elapsed_time >= config.GAME_DURATION:
            self.game_state = "game_over"
            return
        
        # Spawn new zombies
        if (current_time - self.last_zombie_spawn > config.ZOMBIE_SPAWN_RATE and 
            len(self.zombies) < config.MAX_ZOMBIES):
            self.spawn_zombie()
            self.last_zombie_spawn = current_time
        
        # Update zombies
        zombies_to_remove = []
        for zombie in self.zombies:
            zombie.update()
            if not zombie.alive:
                if not zombie.clicked:  # Zombie disappeared without being clicked
                    self.misses += 1
                zombies_to_remove.append(zombie)
        
        # Remove dead zombies
        for zombie in zombies_to_remove:
            self.zombies.remove(zombie)
    
    def spawn_zombie(self):
        """Spawn a new zombie at random position"""
        x, y = get_random_position()
        zombie = Zombie(x, y)
        self.zombies.add(zombie)
    
    def get_remaining_time(self):
        """Get remaining game time"""
        if self.game_state != "playing":
            return 0
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.game_start_time) / 1000
        return max(0, config.GAME_DURATION - int(elapsed_time))

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        if self.game_state == "start":
            self.ui.draw_start_screen(self.screen)
        
        elif self.game_state == "playing":
            # Draw zombies
            for zombie in self.zombies:
                zombie.draw(self.screen)
            
            # Draw UI
            self.ui.draw_score(self.screen, self.score)
            self.ui.draw_misses(self.screen, self.misses)
            self.ui.draw_time(self.screen, self.get_remaining_time())
            
            # Draw weapon swing effect
            if self.last_click_pos:
                self.weapon_cursor.draw_swing_effect(self.screen, self.last_click_pos)
        
        elif self.game_state == "game_over":
            # Draw zombies (frozen)
            for zombie in self.zombies:
                zombie.draw(self.screen)
            
            # Draw game over screen
            self.ui.draw_game_over(self.screen, self.score, self.misses)
        
        pygame.display.flip()
