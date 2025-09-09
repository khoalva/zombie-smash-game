import pygame

class WeaponCursor:
    def __init__(self):
        self.cursor_type = "hammer"
        self.create_hammer_cursor()
        
        # Animation for weapon swing
        self.is_swinging = False
        self.swing_timer = 0
        self.swing_duration = 200  # milliseconds
        
    def create_hammer_cursor(self):
        """Create a hammer-shaped cursor"""
        try:
            # Try to use crosshair cursor as it's more reliable across platforms
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        except:
            # Ultimate fallback
            pass
    
    def create_crosshair_cursor(self):
        """Fallback to crosshair cursor"""
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    
    def start_swing_animation(self):
        """Start weapon swing animation"""
        self.is_swinging = True
        self.swing_timer = pygame.time.get_ticks()
    
    def update(self):
        """Update cursor animation"""
        if self.is_swinging:
            current_time = pygame.time.get_ticks()
            if current_time - self.swing_timer > self.swing_duration:
                self.is_swinging = False
    
    def draw_swing_effect(self, screen, pos):
        """Draw swing effect at cursor position"""
        if self.is_swinging:
            current_time = pygame.time.get_ticks()
            progress = (current_time - self.swing_timer) / self.swing_duration
            
            if progress <= 1.0:
                # Multiple impact rings for more dramatic effect
                for i in range(3):
                    ring_progress = progress + (i * 0.1)
                    if ring_progress <= 1.0:
                        radius = int(25 * ring_progress)
                        alpha = int(200 * (1 - ring_progress))
                        
                        if radius > 0 and alpha > 0:
                            # Different colors for each ring
                            colors = [
                                (255, 255, 100, alpha),  # Bright yellow
                                (255, 200, 50, alpha),   # Orange-yellow  
                                (255, 150, 0, alpha)     # Orange
                            ]
                            
                            color = colors[i % len(colors)]
                            
                            # Draw outer ring
                            pygame.draw.circle(screen, color[:3], pos, radius, 3)
                            
                            # Draw inner filled circle for first ring
                            if i == 0 and radius > 5:
                                inner_color = (255, 255, 150, min(255, alpha + 50))
                                pygame.draw.circle(screen, inner_color[:3], pos, radius - 3, 0)
                
                # Add some spark effects
                if progress < 0.3:  # Only in early phase
                    import random
                    for _ in range(8):
                        angle = random.uniform(0, 6.28)  # 2*pi
                        distance = random.randint(15, 35)
                        spark_x = pos[0] + int(distance * pygame.math.Vector2(1, 0).rotate_rad(angle).x)
                        spark_y = pos[1] + int(distance * pygame.math.Vector2(1, 0).rotate_rad(angle).y)
                        
                        spark_alpha = int(255 * (1 - progress * 3))
                        if spark_alpha > 0:
                            spark_color = (255, 255, 200)
                            pygame.draw.circle(screen, spark_color, (spark_x, spark_y), 2)
