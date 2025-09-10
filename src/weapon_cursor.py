import pygame
import os
import config
from utils import load_image

class WeaponCursor:
    def __init__(self):
        self.cursor_type = "sword"
        self.load_sword_images()
        
        # Animation for weapon swing
        self.is_swinging = False
        self.swing_timer = 0
        self.swing_duration = 300  # milliseconds
        self.sword_angle = 0
        
        # Cursor drawing fallback
        self.use_custom_draw = True  # Always use custom drawing for better control
        
    def load_sword_images(self):
        """Load sword images and create custom cursor"""
        try:
            # Load sword image from the sword folder
            self.sword_image = load_image("sword/Icon28_02.png")
            print(f"Successfully loaded sword image: {self.sword_image.get_size()}")
            
            # Scale sword for cursor size (adjust size as needed)
            cursor_size = (50, 50)  # Make it larger for better visibility
            self.sword_image = pygame.transform.scale(self.sword_image, cursor_size)
            
            # Store original for rotation
            self.original_sword = self.sword_image.copy()
            
            # Hide default cursor and use custom drawing
            pygame.mouse.set_visible(False)
            self.use_custom_draw = True
            print("Sword cursor loaded successfully")
            
        except Exception as e:
            print(f"Could not load sword image: {e}")
            print(f"Full path attempted: {os.path.join(config.IMG_DIR, 'sword/Icon28_01.png')}")
            print("Creating fallback sword cursor...")
            
            # Fallback: create a better looking sword shape
            cursor_size = (50, 50)
            self.sword_image = pygame.Surface(cursor_size, pygame.SRCALPHA)
            
            # Draw a more detailed and visible sword
            # Blade (bigger and brighter)
            pygame.draw.polygon(self.sword_image, (240, 240, 240), [
                (22, 2), (28, 2), (25, 30)
            ])
            # Blade edge highlight
            pygame.draw.line(self.sword_image, (255, 255, 255), (23, 3), (25, 28), 2)
            
            # Guard (more prominent)
            pygame.draw.rect(self.sword_image, (160, 82, 45), (18, 30, 14, 4))
            # Handle (longer and more visible)
            pygame.draw.rect(self.sword_image, (139, 69, 19), (22, 34, 6, 12))
            # Pommel (bigger)
            pygame.draw.circle(self.sword_image, (100, 100, 100), (25, 47), 4)
            
            # Add outline for better visibility
            pygame.draw.polygon(self.sword_image, (0, 0, 0), [
                (22, 2), (28, 2), (25, 30)
            ], 2)
            
            self.original_sword = self.sword_image.copy()
            
            # Hide default cursor
            pygame.mouse.set_visible(False)
            self.use_custom_draw = True
            print("Fallback sword cursor created")
    
    def start_swing_animation(self):
        """Start weapon swing animation"""
        self.is_swinging = True
        self.swing_timer = pygame.time.get_ticks()
        self.sword_angle = 0
    
    def update(self):
        """Update cursor animation"""
        if self.is_swinging:
            current_time = pygame.time.get_ticks()
            if current_time - self.swing_timer > self.swing_duration:
                self.is_swinging = False
                self.sword_angle = 0
            else:
                # Calculate swing angle (smooth arc motion)
                progress = (current_time - self.swing_timer) / self.swing_duration
                # Use sine wave for smoother animation
                import math
                self.sword_angle = math.sin(progress * math.pi) * 90  # 0 to 90 and back
    
    def draw_cursor(self, screen):
        """Draw custom cursor at mouse position"""
        if self.use_custom_draw:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.is_swinging:
                # Draw swinging sword with rotation
                rotated_sword = pygame.transform.rotate(self.original_sword, self.sword_angle)
                sword_rect = rotated_sword.get_rect()
                sword_rect.center = mouse_pos
                screen.blit(rotated_sword, sword_rect)
                
                # Add swing trail effect
                self.draw_swing_trail(screen, mouse_pos)
            else:
                # Draw normal sword cursor
                sword_rect = self.sword_image.get_rect()
                sword_rect.center = mouse_pos
                screen.blit(self.sword_image, sword_rect)
    
    def draw_swing_trail(self, screen, pos):
        """Draw swing trail effect"""
        current_time = pygame.time.get_ticks()
        progress = (current_time - self.swing_timer) / self.swing_duration
        
        if progress < 0.5:  # Show trail in first half of swing
            trail_alpha = int(100 * (1 - progress * 2))  # Fade out
            if trail_alpha > 0:
                # Create trail surface with alpha
                trail_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
                pygame.draw.arc(trail_surface, (255, 255, 0, trail_alpha), 
                               (10, 10, 40, 40), 0, 1.57, 3)  # Quarter circle arc
                trail_rect = trail_surface.get_rect()
                trail_rect.center = pos
                screen.blit(trail_surface, trail_rect)
    
    def draw_swing_effect(self, screen, pos):
        """Draw sword swing effect at cursor position"""
        if self.is_swinging:
            current_time = pygame.time.get_ticks()
            progress = (current_time - self.swing_timer) / self.swing_duration
            
            # Impact effect at the beginning
            if progress < 0.3:
                impact_alpha = int(255 * (1 - progress * 3.33))
                if impact_alpha > 0:
                    impact_radius = int(20 + progress * 15)
                    # Create impact surface with alpha
                    impact_surface = pygame.Surface((impact_radius * 2, impact_radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(impact_surface, (255, 255, 100, impact_alpha), 
                                     (impact_radius, impact_radius), impact_radius, 3)
                    impact_rect = impact_surface.get_rect()
                    impact_rect.center = pos
                    screen.blit(impact_surface, impact_rect)