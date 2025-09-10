"""
Main game class for Zombie Whacker Game
"""
import pygame
from typing import Optional

import config
from utils import load_image, get_random_position
from sprites.zombie import Zombie
from ui import GameUI
from weapon_cursor import WeaponCursor
from sound_manager import SoundManager
from game_state import GameStateManager
from input_handler import InputHandler

class Game:
    """Main game class handling game loop and state management"""
    
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Zombie Whacker Game")

        # Core game components
        self.clock = pygame.time.Clock()
        self.running = True
        self.state_manager = GameStateManager()
        
        # Initialize systems
        self.sound_manager = SoundManager()
        self.input_handler = InputHandler(self)
        
        # Audio settings
        self.music_volume = self.sound_manager.get_music_volume()
        self.sound_volume = self.sound_manager.get_sound_volume()
        
        # Game objects
        self.zombies = pygame.sprite.Group()
        self.ui = GameUI()
        self.weapon_cursor = WeaponCursor()
        
        # Game state variables
        self.score = 0
        self.misses = 0
        self.game_start_time = 0
        self.last_zombie_spawn = 0
        self.last_click_pos: Optional[tuple] = None
        self.last_click_time = 0
        
        # Initialize graphics
        self._load_background()
    
    def _load_background(self) -> None:
        """Load background image with fallback"""
        try:
            self.background = load_image("background/background_2.jpg", convert_alpha=False)
            self.background = pygame.transform.scale(
                self.background, 
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
            )
        except Exception as e:
            print(f"Could not load background image: {e}")
            self.background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))  # Dark gray background
        
    def start_background_music(self) -> None:
        """Start playing background music"""
        self.sound_manager.start_background_music()
    
    def stop_background_music(self) -> None:
        """Stop background music"""
        self.sound_manager.stop_background_music()
        
    def reset_game(self) -> None:
        """Reset game for new round"""
        self.zombies.empty()
        self.score = 0
        self.misses = 0
        self.game_start_time = pygame.time.get_ticks()
        self.last_zombie_spawn = 0
        self.last_click_time = 0
        self.last_click_pos = None
        self.state_manager.set_state(config.GameState.PLAYING)
        
        # Start background music when game starts
        self.start_background_music()

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self.clock.tick(config.FPS)
            self.input_handler.handle_events()
            self.update()
            self.draw()
        
        # Clean up when exiting
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources when exiting"""
        self.sound_manager.cleanup()
    
    def handle_click(self, pos: tuple) -> None:
        """Handle mouse click on zombies"""
        self.last_click_pos = pos
        self.weapon_cursor.start_swing_animation()
        
        # Find the zombie that was clicked (if any)
        hit_zombie = self._check_zombie_hits(pos)
        
        # Play appropriate sound
        sound_type = config.SoundType.HIT.value if hit_zombie else config.SoundType.MISS.value
        self.sound_manager.play_sound(sound_type)
    
    def _check_zombie_hits(self, pos: tuple) -> bool:
        """Check if click hit any zombies"""
        for zombie in self.zombies:
            if (zombie.rect.collidepoint(pos) and 
                zombie.alive and 
                not zombie.clicked):
                if zombie.on_click():
                    self.score += config.POINTS_PER_HIT
                    return True
        return False
    
    def update(self) -> None:
        """Update game state"""
        if not self.state_manager.is_state(config.GameState.PLAYING):
            return
        
        self.weapon_cursor.update()
        current_time = pygame.time.get_ticks()
        
        # Check if game time is up
        if self._is_game_time_up(current_time):
            self.state_manager.set_state(config.GameState.GAME_OVER)
            self.stop_background_music()
            return
        
        # Spawn new zombies
        self._handle_zombie_spawning(current_time)
        
        # Update and clean up zombies
        self._update_zombies()
    
    def _is_game_time_up(self, current_time: int) -> bool:
        """Check if game time has elapsed"""
        elapsed_time = (current_time - self.game_start_time) / 1000
        return elapsed_time >= config.GAME_DURATION
    
    def _handle_zombie_spawning(self, current_time: int) -> None:
        """Handle zombie spawning logic"""
        # Dynamic spawn rate based on current zombie count
        spawn_rate = config.ZOMBIE_SPAWN_RATE + (len(self.zombies) * 500)
        
        if (current_time - self.last_zombie_spawn > spawn_rate and 
            len(self.zombies) < config.MAX_ZOMBIES):
            self.spawn_zombie()
            self.last_zombie_spawn = current_time
    
    def _update_zombies(self) -> None:
        """Update all zombies and remove dead ones"""
        zombies_to_remove = []
        
        for zombie in self.zombies:
            zombie.update()
            if not zombie.alive:
                if not zombie.clicked:  # Zombie disappeared without being clicked
                    self.misses += 1
                zombies_to_remove.append(zombie)
        
        # Remove dead zombies safely
        for zombie in zombies_to_remove:
            self.zombies.remove(zombie)
    
    def spawn_zombie(self) -> None:
        """Spawn a new zombie at random position"""
        x, y = get_random_position()
        zombie = Zombie(x, y)
        self.zombies.add(zombie)
    
    def get_remaining_time(self) -> int:
        """Get remaining game time in seconds"""
        if not self.state_manager.is_state(config.GameState.PLAYING):
            return 0
        
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.game_start_time) / 1000
        return max(0, config.GAME_DURATION - int(elapsed_time))

    def draw(self) -> None:
        """Render current game state"""
        self.screen.blit(self.background, (0, 0))
        
        current_state = self.state_manager.get_state()
        
        if current_state == config.GameState.MENU:
            self._draw_menu()
        elif current_state == config.GameState.PLAYING:
            self._draw_playing()
        elif current_state == config.GameState.GAME_OVER:
            self._draw_game_over()
        
        pygame.display.flip()
    
    def _draw_menu(self) -> None:
        """Draw menu state"""
        if self.ui.in_settings:
            self.ui.draw_settings_menu(self.screen, self.music_volume, self.sound_volume)
        else:
            self.ui.draw_main_menu(self.screen)
    
    def _draw_playing(self) -> None:
        """Draw playing state"""
        # Draw zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Draw UI elements
        self.ui.draw_score(self.screen, self.score)
        self.ui.draw_misses(self.screen, self.misses)
        self.ui.draw_time(self.screen, self.get_remaining_time())
        
        # Draw weapon effects
        if self.last_click_pos:
            self.weapon_cursor.draw_swing_effect(self.screen, self.last_click_pos)
        
        self.weapon_cursor.draw_cursor(self.screen)
    
    def _draw_game_over(self) -> None:
        """Draw game over state"""
        # Draw frozen zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Draw game over screen
        self.ui.draw_game_over(self.screen, self.score, self.misses)
