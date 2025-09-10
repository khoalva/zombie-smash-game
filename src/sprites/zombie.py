import pygame
import random
import os
from utils import load_image
import config

# Cache for shared sprite images to reduce memory usage
_sprite_cache = {
    'idle_frames': None,
    'hurt_frames': None,
    'dying_frames': None
}

def load_shared_animations():
    """Load animation frames once and share between all zombies"""
    if _sprite_cache['idle_frames'] is not None:
        return _sprite_cache
    
    try:
        # Load idle animation
        idle_frames = []
        idle_path = os.path.join(config.IMG_DIR, "zombie", "Idle")
        if os.path.exists(idle_path):
            idle_files = sorted([f for f in os.listdir(idle_path) if f.endswith('.png')])[:config.FRAME_LIMIT_IDLE]
            for file in idle_files:
                img = load_image(f"zombie/Idle/{file}")
                img = pygame.transform.scale(img, (120, 120))
                idle_frames.append(img)
        
        # Load hurt animation
        hurt_frames = []
        hurt_path = os.path.join(config.IMG_DIR, "zombie", "Hurt")
        if os.path.exists(hurt_path):
            hurt_files = sorted([f for f in os.listdir(hurt_path) if f.endswith('.png')])[:config.FRAME_LIMIT_HURT]
            for file in hurt_files:
                img = load_image(f"zombie/Hurt/{file}")
                img = pygame.transform.scale(img, (120, 120))
                hurt_frames.append(img)
        
        # Load dying animation
        dying_frames = []
        dying_path = os.path.join(config.IMG_DIR, "zombie", "Dying")
        if os.path.exists(dying_path):
            dying_files = sorted([f for f in os.listdir(dying_path) if f.endswith('.png')])[:config.FRAME_LIMIT_DYING]
            for file in dying_files:
                img = load_image(f"zombie/Dying/{file}")
                img = pygame.transform.scale(img, (120, 120))
                dying_frames.append(img)
        
        _sprite_cache['idle_frames'] = idle_frames
        _sprite_cache['hurt_frames'] = hurt_frames
        _sprite_cache['dying_frames'] = dying_frames
        
    except Exception as e:
        print(f"Error loading zombie animations: {e}")
        # Fallback sprites
        size = (120, 120)
        idle_surf = pygame.Surface(size)
        idle_surf.fill((0, 255, 0))
        hurt_surf = pygame.Surface(size)
        hurt_surf.fill((255, 255, 0))
        dying_surf = pygame.Surface(size)
        dying_surf.fill((255, 0, 0))
        
        _sprite_cache['idle_frames'] = [idle_surf]
        _sprite_cache['hurt_frames'] = [hurt_surf]
        _sprite_cache['dying_frames'] = [dying_surf]
    
    return _sprite_cache

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Position
        self.x = x
        self.y = y
        
        # Use shared animation frames to save memory
        shared_animations = load_shared_animations()
        self.idle_frames = shared_animations['idle_frames']
        self.hurt_frames = shared_animations['hurt_frames']
        self.dying_frames = shared_animations['dying_frames']
        
        # Current animation state
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = config.ANIMATION_SPEED
        self.frame_timer = 0
        
        # Sprite properties
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Game properties
        self.alive = True
        self.clicked = False
        self.appear_time = pygame.time.get_ticks()
        self.lifetime = random.randint(config.ZOMBIE_LIFETIME_MIN, config.ZOMBIE_LIFETIME_MAX)
        
        # State for dying animation
        self.dying = False
        self.hurt_timer = 0
        

    
    def update(self):
        """Update zombie animation and state"""
        if not self.alive:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Check if zombie should disappear (missed)
        if not self.clicked and current_time - self.appear_time > self.lifetime:
            self.alive = False
            return
        
        # Handle hurt state - faster transition to dying
        if self.current_animation == "hurt" and current_time - self.hurt_timer > config.ZOMBIE_HURT_DURATION:
            self.current_animation = "dying"
            self.frame_index = 0
            self.frame_timer = 0
        
        # Handle dying animation - ensure zombie dies quickly
        if self.current_animation == "dying":
            if self.frame_index >= len(self.dying_frames) - 1:
                self.alive = False
                return
            # Force death after short time to prevent lag
            elif current_time - self.hurt_timer > config.ZOMBIE_DEATH_TIMEOUT:
                self.alive = False
                return
        
        # Update animation frame - only update when timer reaches threshold
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            frame_changed = False
            
            if self.current_animation == "idle" and len(self.idle_frames) > 0:
                old_frame = self.frame_index
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                if old_frame != self.frame_index:
                    self.image = self.idle_frames[self.frame_index]
                    frame_changed = True
                    
            elif self.current_animation == "hurt" and len(self.hurt_frames) > 0:
                if self.frame_index < len(self.hurt_frames) - 1:
                    self.frame_index += 1
                    self.image = self.hurt_frames[self.frame_index]
                    frame_changed = True
                    
            elif self.current_animation == "dying" and len(self.dying_frames) > 0:
                if self.frame_index < len(self.dying_frames) - 1:
                    self.frame_index += 1
                    self.image = self.dying_frames[self.frame_index]
                    frame_changed = True
                else:
                    # Ensure zombie dies when animation completes
                    self.alive = False
                    return
    
    def on_click(self):
        """Handle zombie being clicked"""
        if not self.clicked and self.alive:
            self.clicked = True
            self.current_animation = "hurt"
            self.frame_index = 0
            self.frame_timer = 0
            self.hurt_timer = pygame.time.get_ticks()
            return True
        return False
    
    def draw(self, screen):
        """Draw zombie on screen"""
        if self.alive:
            screen.blit(self.image, self.rect)
