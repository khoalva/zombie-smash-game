import pygame
import config

class GameUI:
    def __init__(self):
        # Initialize font (sử dụng font mặc định nếu chưa có font asset)
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Use color constants from config
        self.colors = config.Colors
        
        # UI positions
        self.score_pos = (20, 20)
        self.miss_pos = (20, 60)
        self.time_pos = (config.SCREEN_WIDTH - 150, 20)
        
        # Menu system
        self.menu_items = ["START GAME", "SETTINGS", "QUIT"]
        self.settings_items = ["MUSIC VOLUME", "SOUND EFFECTS", "BACK"]
        self.selected_item = 0
        self.in_settings = False
        
    def draw_score(self, screen, score):
        """Draw current score"""
        score_text = self.font_medium.render(f"Score: {score}", True, self.colors.GREEN)
        screen.blit(score_text, self.score_pos)
    
    def draw_misses(self, screen, misses):
        """Draw miss count"""
        miss_text = self.font_medium.render(f"Miss: {misses}", True, self.colors.RED)
        screen.blit(miss_text, self.miss_pos)
    
    def draw_time(self, screen, remaining_time):
        """Draw remaining time"""
        time_text = self.font_medium.render(f"Time: {remaining_time}", True, self.colors.WHITE)
        screen.blit(time_text, self.time_pos)
    
    def draw_game_over(self, screen, final_score, total_misses):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.colors.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER!", True, self.colors.RED)
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 60))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {final_score}", True, self.colors.WHITE)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 10))
        screen.blit(score_text, score_rect)
        
        # Total misses
        miss_text = self.font_medium.render(f"Total Misses: {total_misses}", True, self.colors.WHITE)
        miss_rect = miss_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 30))
        screen.blit(miss_text, miss_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press SPACE to return to menu or ESC to quit", True, self.colors.YELLOW)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 80))
        screen.blit(restart_text, restart_rect)
    
    def draw_main_menu(self, screen):
        """Draw main menu"""
        # Title with shadow effect
        title_shadow = self.font_large.render("ZOMBIE WHACKER", True, self.colors.BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(config.SCREEN_WIDTH//2 + 3, config.SCREEN_HEIGHT//2 - 117))
        screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.font_large.render("ZOMBIE WHACKER", True, self.colors.RED)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 120))
        screen.blit(title_text, title_rect)
        
        # Menu items
        menu_start_y = config.SCREEN_HEIGHT//2 - 30
        for i, item in enumerate(self.menu_items):
            color = self.colors.YELLOW if i == self.selected_item else self.colors.WHITE
            text = self.font_medium.render(item, True, color)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH//2, menu_start_y + i * 50))
            
            # Draw selection highlight
            if i == self.selected_item:
                highlight_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 5, 
                                           text_rect.width + 20, text_rect.height + 10)
                pygame.draw.rect(screen, self.colors.DARK_GRAY, highlight_rect)
                pygame.draw.rect(screen, self.colors.YELLOW, highlight_rect, 2)
            
            screen.blit(text, text_rect)
        
        # Instructions
        instruction_text = self.font_small.render("Use UP/DOWN arrows and ENTER to navigate", True, self.colors.GRAY)
        instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_settings_menu(self, screen, music_volume, sound_volume):
        """Draw settings menu"""
        # Title with shadow effect
        title_shadow = self.font_large.render("SETTINGS", True, self.colors.BLACK)
        title_shadow_rect = title_shadow.get_rect(center=(config.SCREEN_WIDTH//2 + 3, config.SCREEN_HEIGHT//2 - 117))
        screen.blit(title_shadow, title_shadow_rect)
        
        title_text = self.font_large.render("SETTINGS", True, self.colors.BLUE)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 120))
        screen.blit(title_text, title_rect)
        
        # Settings items
        settings_start_y = config.SCREEN_HEIGHT//2 - 50
        
        for i, item in enumerate(self.settings_items):
            color = self.colors.YELLOW if i == self.selected_item else self.colors.WHITE
            
            # Draw selection highlight
            if i == self.selected_item:
                highlight_rect = pygame.Rect(config.SCREEN_WIDTH//2 - 200, 
                                           settings_start_y + i * 60 - 5,
                                           400, 50)
                pygame.draw.rect(screen, self.colors.DARK_GRAY, highlight_rect)
                pygame.draw.rect(screen, self.colors.YELLOW, highlight_rect, 2)
            
            if item == "MUSIC VOLUME":
                # Draw music volume control
                text = self.font_medium.render("MUSIC VOLUME", True, color)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH//2 - 100, settings_start_y + i * 60))
                screen.blit(text, text_rect)
                
                # Volume bar
                bar_x = config.SCREEN_WIDTH//2 + 50
                bar_y = settings_start_y + i * 60 - 10
                bar_width = 150
                bar_height = 20
                
                # Background bar
                pygame.draw.rect(screen, self.colors.GRAY, (bar_x, bar_y, bar_width, bar_height))
                # Volume bar
                volume_width = int(bar_width * music_volume)
                pygame.draw.rect(screen, self.colors.GREEN, (bar_x, bar_y, volume_width, bar_height))
                # Border
                pygame.draw.rect(screen, self.colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                
                # Volume percentage
                volume_text = self.font_small.render(f"{int(music_volume * 100)}%", True, self.colors.WHITE)
                screen.blit(volume_text, (bar_x + bar_width + 10, bar_y))
                
            elif item == "SOUND EFFECTS":
                # Draw sound effects volume control
                text = self.font_medium.render("SOUND EFFECTS", True, color)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH//2 - 100, settings_start_y + i * 60))
                screen.blit(text, text_rect)
                
                # Volume bar
                bar_x = config.SCREEN_WIDTH//2 + 50
                bar_y = settings_start_y + i * 60 - 10
                bar_width = 150
                bar_height = 20
                
                # Background bar
                pygame.draw.rect(screen, self.colors.GRAY, (bar_x, bar_y, bar_width, bar_height))
                # Volume bar
                volume_width = int(bar_width * sound_volume)
                pygame.draw.rect(screen, self.colors.BLUE, (bar_x, bar_y, volume_width, bar_height))
                # Border
                pygame.draw.rect(screen, self.colors.WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                
                # Volume percentage
                volume_text = self.font_small.render(f"{int(sound_volume * 100)}%", True, self.colors.WHITE)
                screen.blit(volume_text, (bar_x + bar_width + 10, bar_y))
                
            else:  # BACK button
                text = self.font_medium.render(item, True, color)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH//2, settings_start_y + i * 60))
                screen.blit(text, text_rect)
        
        # Instructions
        if self.selected_item < 2:  # Volume controls
            instruction_text = self.font_small.render("Use LEFT/RIGHT arrows to adjust volume", True, self.colors.GRAY)
        else:  # Back button
            instruction_text = self.font_small.render("Press ENTER to go back", True, self.colors.GRAY)
        instruction_rect = instruction_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def draw_start_screen(self, screen):
        """Draw start screen (kept for compatibility)"""
        self.draw_main_menu(screen)
    
    def handle_menu_input(self, key):
        """Handle menu navigation input"""
        if not self.in_settings:
            # Main menu navigation
            if key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif key == pygame.K_RETURN:
                return self.menu_items[self.selected_item]
        else:
            # Settings menu navigation
            if key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.settings_items)
            elif key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.settings_items)
            elif key == pygame.K_RETURN and self.selected_item == 2:  # BACK
                self.in_settings = False
                self.selected_item = 0
                return "BACK"
            elif key == pygame.K_LEFT:
                if self.selected_item == 0:  # Music volume
                    return "MUSIC_DOWN"
                elif self.selected_item == 1:  # Sound effects
                    return "SOUND_DOWN"
            elif key == pygame.K_RIGHT:
                if self.selected_item == 0:  # Music volume
                    return "MUSIC_UP"
                elif self.selected_item == 1:  # Sound effects
                    return "SOUND_UP"
        
        return None
    
    def enter_settings(self):
        """Enter settings menu"""
        self.in_settings = True
        self.selected_item = 0
