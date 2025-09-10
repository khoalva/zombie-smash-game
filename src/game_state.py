"""
Game state manager for handling different game states and transitions
"""
from enum import Enum
import config

class GameStateManager:
    def __init__(self):
        self.current_state = config.GameState.MENU
        self.previous_state = None
    
    def set_state(self, new_state: config.GameState):
        """Set new game state"""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
    
    def is_state(self, state: config.GameState) -> bool:
        """Check if current state matches given state"""
        return self.current_state == state
    
    def get_state(self) -> config.GameState:
        """Get current state"""
        return self.current_state
    
    def get_previous_state(self) -> config.GameState:
        """Get previous state"""
        return self.previous_state
