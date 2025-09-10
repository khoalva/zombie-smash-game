import pygame
import pygame.mixer
import random
import os
import config
from utils import load_image, get_random_position
from sprites.zombie import Zombie
from ui import GameUI
from weapon_cursor import WeaponCursor
from sound_manager import SoundManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Zombie Whacker Game")

        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game states
        self.game_state = "menu"  # menu, playing, game_over
        
        # Load background (fallback to solid color if not available)
        try:
            self.background = load_image("background/background_2.jpg", convert_alpha=False)
            self.background = pygame.transform.scale(self.background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            self.background.fill((50, 50, 50))  # Dark gray background
        
        # Initialize sound system
        self.sound_manager = SoundManager()
        self.init_sound()
        
        # Audio settings (after sound_manager is initialized)
        self.music_volume = self.sound_manager.get_music_volume()
        self.sound_volume = self.sound_manager.get_sound_volume()
        
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
        self.last_click_time = 0
        
    def init_sound(self):
        """Initialize sound system and load background music"""
        self.sound_enabled = False
        self.background_music_loaded = False
        
        try:
            # Check if mixer is available
            if not pygame.mixer.get_init():
                print("Audio mixer not initialized - running without sound")
                return
            
            self.sound_enabled = True
            
            # Try to load background music
            music_files = [
                "sound_1.wav",  # Use existing sound file
                "background_music.mp3",
                "background_music.wav",
                "background_music.ogg",
                "music.mp3",
                "music.wav"
            ]
            
            for music_file in music_files:
                try:
                    music_path = os.path.join(config.SOUND_DIR, music_file)
                    if os.path.exists(music_path):
                        pygame.mixer.music.load(music_path)
                        self.background_music_loaded = True
                        print(f"Loaded background music: {music_file}")
                        break
                except Exception as e:
                    print(f"Could not load {music_file}: {e}")
                    continue
            
            if not self.background_music_loaded:
                print("No background music found in assets/sounds/")
            elif self.sound_enabled:
                # Set initial volume only if sound is enabled
                pygame.mixer.music.set_volume(config.DEFAULT_MUSIC_VOLUME)
                
        except Exception as e:
            print(f"Could not initialize sound: {e}")
            self.sound_enabled = False
            self.background_music_loaded = False
    
    def start_background_music(self):
        """Start playing background music"""
        if self.sound_enabled and self.background_music_loaded:
            try:
                pygame.mixer.music.play(-1)  # Loop indefinitely
                print("Background music started")
            except Exception as e:
                print(f"Could not start background music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        if self.sound_enabled:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def update_music_volume(self):
        """Update music volume (legacy method, now handled by sound_manager)"""
        self.sound_manager.set_music_volume(self.music_volume)
        
    def reset_game(self):
        """Reset game for new round"""
        self.zombies.empty()
        self.score = 0
        self.misses = 0
        self.game_start_time = pygame.time.get_ticks()
        self.last_zombie_spawn = 0
        self.last_click_time = 0
        self.game_state = "playing"
        
        # Start background music when game starts
        self.start_background_music()

    def run(self):
        while self.running:
            self.clock.tick(config.FPS)
            self.handle_events()
            self.update()
            self.draw()
        
        # Clean up when exiting
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources when exiting"""
        self.stop_background_music()
        if self.sound_enabled:
            try:
                pygame.mixer.quit()
            except:
                pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "menu":
                    menu_action = self.ui.handle_menu_input(event.key)
                    if menu_action == "START GAME":
                        self.sound_manager.play_sound('click')
                        self.reset_game()
                    elif menu_action == "SETTINGS":
                        self.sound_manager.play_sound('click')
                        self.ui.enter_settings()
                    elif menu_action == "QUIT":
                        self.sound_manager.play_sound('click')
                        self.running = False
                    elif menu_action == "MUSIC_UP":
                        self.music_volume = min(1.0, self.music_volume + config.VOLUME_STEP)
                        self.sound_manager.set_music_volume(self.music_volume)
                        self.sound_manager.play_sound('click')
                    elif menu_action == "MUSIC_DOWN":
                        self.music_volume = max(0.0, self.music_volume - config.VOLUME_STEP)
                        self.sound_manager.set_music_volume(self.music_volume)
                        self.sound_manager.play_sound('click')
                    elif menu_action == "SOUND_UP":
                        self.sound_volume = min(1.0, self.sound_volume + config.VOLUME_STEP)
                        self.sound_manager.set_sound_volume(self.sound_volume)
                        self.sound_manager.play_sound('click')
                    elif menu_action == "SOUND_DOWN":
                        self.sound_volume = max(0.0, self.sound_volume - config.VOLUME_STEP)
                        self.sound_manager.set_sound_volume(self.sound_volume)
                        self.sound_manager.play_sound('click')
                elif event.key == pygame.K_SPACE:
                    if self.game_state == "game_over":
                        self.game_state = "menu"
                        self.ui.selected_item = 0
                        self.ui.in_settings = False
                elif event.key == pygame.K_ESCAPE:
                    if self.game_state == "game_over":
                        self.game_state = "menu"
                        self.ui.selected_item = 0
                        self.ui.in_settings = False
                    elif self.game_state == "playing":
                        self.game_state = "menu"
                        self.stop_background_music()
                        self.ui.selected_item = 0
                        self.ui.in_settings = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "playing" and event.button == 1:  # Left click
                    current_time = pygame.time.get_ticks()
                    # Add cooldown to prevent spam clicking issues
                    if current_time - self.last_click_time > 100:  # Increased cooldown to 100ms
                        self.handle_click(event.pos)
                        self.last_click_time = current_time
    
    def handle_click(self, pos):
        """Handle mouse click on zombies"""
        self.last_click_pos = pos
        self.weapon_cursor.start_swing_animation()
        
        # Find the zombie that was clicked (if any)
        hit_zombie = False
        for zombie in self.zombies:
            if zombie.rect.collidepoint(pos) and zombie.alive and not zombie.clicked:
                if zombie.on_click():
                    self.score += config.POINTS_PER_HIT
                    hit_zombie = True
                    self.sound_manager.play_sound('hit')
                    break  # Only hit one zombie per click
        
        # Play miss sound if no zombie was hit
        if not hit_zombie:
            self.sound_manager.play_sound('miss')
    
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
            self.stop_background_music()  # Stop music when game ends
            return
        
        # Spawn new zombies with dynamic spawn rate based on current zombie count
        spawn_rate = config.ZOMBIE_SPAWN_RATE + (len(self.zombies) * 500)  # Slower spawn when more zombies
        if (current_time - self.last_zombie_spawn > spawn_rate and 
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
            try:
                self.zombies.remove(zombie)
            except ValueError:
                pass  # Zombie already removed, ignore error
    
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
        
        if self.game_state == "menu":
            if self.ui.in_settings:
                self.ui.draw_settings_menu(self.screen, self.music_volume, self.sound_volume)
            else:
                self.ui.draw_main_menu(self.screen)
        
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
            
            # Draw weapon cursor
            self.weapon_cursor.draw_cursor(self.screen)
        
        elif self.game_state == "game_over":
            # Draw zombies (frozen)
            for zombie in self.zombies:
                zombie.draw(self.screen)
            
            # Draw game over screen
            self.ui.draw_game_over(self.screen, self.score, self.misses)
        
        pygame.display.flip()
