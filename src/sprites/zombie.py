import pygame
import random
import os
from utils import load_image
import config

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Position
        self.x = x
        self.y = y
        
        # Animation
        self.idle_frames = []
        self.hurt_frames = []
        self.dying_frames = []
        
        # Load animation frames
        self.load_animations()
        
        # Current animation state
        self.current_animation = "idle"
        self.frame_index = 0
        self.animation_speed = 0.3  # Increased from 0.15 to make animation faster
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
        self.lifetime = random.randint(2000, 4000)  # 2-4 seconds
        
        # State for dying animation
        self.dying = False
        self.hurt_timer = 0
        
    def load_animations(self):
        """Load all animation frames"""
        try:
            # Load idle animation
            idle_path = os.path.join(config.IMG_DIR, "zombie", "Idle")
            if os.path.exists(idle_path):
                idle_files = sorted([f for f in os.listdir(idle_path) if f.endswith('.png')])
                for file in idle_files:
                    img = load_image(f"zombie/Idle/{file}")
                    # Scale down zombie to reasonable size
                    img = pygame.transform.scale(img, (120, 120))
                    self.idle_frames.append(img)
            
            # Load hurt animation  
            hurt_path = os.path.join(config.IMG_DIR, "zombie", "Hurt")
            if os.path.exists(hurt_path):
                hurt_files = sorted([f for f in os.listdir(hurt_path) if f.endswith('.png')])
                for file in hurt_files:
                    img = load_image(f"zombie/Hurt/{file}")
                    img = pygame.transform.scale(img, (120, 120))
                    self.hurt_frames.append(img)
            
            # Load dying animation
            dying_path = os.path.join(config.IMG_DIR, "zombie", "Dying")
            if os.path.exists(dying_path):
                dying_files = sorted([f for f in os.listdir(dying_path) if f.endswith('.png')])
                for file in dying_files:
                    img = load_image(f"zombie/Dying/{file}")
                    img = pygame.transform.scale(img, (120, 120))
                    self.dying_frames.append(img)
                    
        except Exception as e:
            print(f"Error loading zombie animations: {e}")
            # Fallback: create simple colored rectangles if images fail to load
            self.create_fallback_sprites()
    
    def create_fallback_sprites(self):
        """Create simple colored rectangles as fallback"""
        size = (120, 120)
        
        # Green for idle
        idle_surf = pygame.Surface(size)
        idle_surf.fill((0, 255, 0))
        self.idle_frames = [idle_surf]
        
        # Yellow for hurt
        hurt_surf = pygame.Surface(size)
        hurt_surf.fill((255, 255, 0))
        self.hurt_frames = [hurt_surf]
        
        # Red for dying
        dying_surf = pygame.Surface(size)
        dying_surf.fill((255, 0, 0))
        self.dying_frames = [dying_surf]
    
    def update(self):
        """Update zombie animation and state"""
        if not self.alive:
            return
            
        current_time = pygame.time.get_ticks()
        
        # Check if zombie should disappear (missed)
        if not self.clicked and current_time - self.appear_time > self.lifetime:
            self.alive = False
            return
        
        # Handle hurt state - reduced time from 300ms to 150ms
        if self.current_animation == "hurt" and current_time - self.hurt_timer > 150:
            self.current_animation = "dying"
            self.frame_index = 0
            self.frame_timer = 0
        
        # Handle dying animation
        if self.current_animation == "dying":
            if self.frame_index >= len(self.dying_frames) - 1:
                self.alive = False
                return
        
        # Update animation frame
        self.frame_timer += self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            
            if self.current_animation == "idle":
                self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.frame_index]
            elif self.current_animation == "hurt":
                if self.frame_index < len(self.hurt_frames) - 1:
                    self.frame_index += 1
                self.image = self.hurt_frames[self.frame_index]
            elif self.current_animation == "dying":
                if self.frame_index < len(self.dying_frames) - 1:
                    self.frame_index += 1
                self.image = self.dying_frames[self.frame_index]
    
    def on_click(self):
        """Handle zombie being clicked"""
        if not self.clicked and self.alive and self.current_animation == "idle":
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
