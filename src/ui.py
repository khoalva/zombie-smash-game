import pygame
import config

class GameUI:
    def __init__(self):
        # Initialize font (sử dụng font mặc định nếu chưa có font asset)
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.yellow = (255, 255, 0)
        
        # UI positions
        self.score_pos = (20, 20)
        self.miss_pos = (20, 60)
        self.time_pos = (config.SCREEN_WIDTH - 150, 20)
        
    def draw_score(self, screen, score):
        """Draw current score"""
        score_text = self.font_medium.render(f"Score: {score}", True, self.green)
        screen.blit(score_text, self.score_pos)
    
    def draw_misses(self, screen, misses):
        """Draw miss count"""
        miss_text = self.font_medium.render(f"Miss: {misses}", True, self.red)
        screen.blit(miss_text, self.miss_pos)
    
    def draw_time(self, screen, remaining_time):
        """Draw remaining time"""
        time_text = self.font_medium.render(f"Time: {remaining_time}", True, self.white)
        screen.blit(time_text, self.time_pos)
    
    def draw_game_over(self, screen, final_score, total_misses):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(self.black)
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER!", True, self.red)
        game_over_rect = game_over_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 60))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = self.font_medium.render(f"Final Score: {final_score}", True, self.white)
        score_rect = score_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 10))
        screen.blit(score_text, score_rect)
        
        # Total misses
        miss_text = self.font_medium.render(f"Total Misses: {total_misses}", True, self.white)
        miss_rect = miss_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 30))
        screen.blit(miss_text, miss_rect)
        
        # Restart instruction
        restart_text = self.font_small.render("Press SPACE to play again or ESC to quit", True, self.yellow)
        restart_rect = restart_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 + 80))
        screen.blit(restart_text, restart_rect)
    
    def draw_start_screen(self, screen):
        """Draw start screen"""
        # Title
        title_text = self.font_large.render("ZOMBIE WHACKER", True, self.red)
        title_rect = title_text.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2 - 80))
        screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Click on zombies to whack them!",
            "Zombies appear randomly for 2-4 seconds",
            "Hit: +10 points",
            "Miss: +1 miss count",
            "",
            "Press SPACE to start!"
        ]
        
        y_offset = config.SCREEN_HEIGHT//2 - 20
        for instruction in instructions:
            if instruction:  # Skip empty lines
                text = self.font_small.render(instruction, True, self.white)
                text_rect = text.get_rect(center=(config.SCREEN_WIDTH//2, y_offset))
                screen.blit(text, text_rect)
            y_offset += 30
