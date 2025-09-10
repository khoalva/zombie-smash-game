"""
Input handler for managing game input events
"""
import pygame
import config
from typing import Optional, Dict, Any

class InputHandler:
    def __init__(self, game):
        self.game = game
        self.key_handlers = {
            config.GameState.MENU: self._handle_menu_input,
            config.GameState.PLAYING: self._handle_playing_input,
            config.GameState.GAME_OVER: self._handle_game_over_input
        }
    
    def handle_events(self) -> None:
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            
            elif event.type == pygame.KEYDOWN:
                current_state = self.game.state_manager.get_state()
                if current_state in self.key_handlers:
                    self.key_handlers[current_state](event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_input(event)
    
    def _handle_menu_input(self, key: int) -> None:
        """Handle menu input events"""
        menu_action = self.game.ui.handle_menu_input(key)
        
        action_handlers = {
            "START GAME": self._start_game,
            "SETTINGS": self._enter_settings,
            "QUIT": self._quit_game,
            "MUSIC_UP": lambda: self._adjust_volume('music', config.VOLUME_STEP),
            "MUSIC_DOWN": lambda: self._adjust_volume('music', -config.VOLUME_STEP),
            "SOUND_UP": lambda: self._adjust_volume('sound', config.VOLUME_STEP),
            "SOUND_DOWN": lambda: self._adjust_volume('sound', -config.VOLUME_STEP),
        }
        
        if menu_action in action_handlers:
            self.game.sound_manager.play_sound(config.SoundType.CLICK.value)
            action_handlers[menu_action]()
    
    def _handle_playing_input(self, key: int) -> None:
        """Handle playing state input events"""
        if key == pygame.K_ESCAPE:
            self._return_to_menu()
    
    def _handle_game_over_input(self, key: int) -> None:
        """Handle game over input events"""
        if key in (pygame.K_SPACE, pygame.K_ESCAPE):
            self._return_to_menu()
    
    def _handle_mouse_input(self, event) -> None:
        """Handle mouse input events"""
        if (self.game.state_manager.is_state(config.GameState.PLAYING) and 
            event.button == 1):  # Left click
            current_time = pygame.time.get_ticks()
            if current_time - self.game.last_click_time > config.CLICK_COOLDOWN:
                self.game.handle_click(event.pos)
                self.game.last_click_time = current_time
    
    def _start_game(self) -> None:
        """Start a new game"""
        self.game.reset_game()
    
    def _enter_settings(self) -> None:
        """Enter settings menu"""
        self.game.ui.enter_settings()
    
    def _quit_game(self) -> None:
        """Quit the game"""
        self.game.running = False
    
    def _adjust_volume(self, volume_type: str, adjustment: float) -> None:
        """Adjust volume levels"""
        if volume_type == 'music':
            new_volume = max(config.MIN_VOLUME, 
                           min(config.MAX_VOLUME, 
                               self.game.music_volume + adjustment))
            self.game.music_volume = new_volume
            self.game.sound_manager.set_music_volume(new_volume)
        elif volume_type == 'sound':
            new_volume = max(config.MIN_VOLUME, 
                           min(config.MAX_VOLUME, 
                               self.game.sound_volume + adjustment))
            self.game.sound_volume = new_volume
            self.game.sound_manager.set_sound_volume(new_volume)
    
    def _return_to_menu(self) -> None:
        """Return to main menu"""
        self.game.state_manager.set_state(config.GameState.MENU)
        self.game.stop_background_music()
        self.game.ui.selected_item = 0
        self.game.ui.in_settings = False
