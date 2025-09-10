from enum import Enum

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Asset directories
ASSET_DIR = "assets/"
IMG_DIR = ASSET_DIR + "images/"
SOUND_DIR = ASSET_DIR + "sounds/"
FONT_DIR = ASSET_DIR + "fonts/"

# Game settings
GAME_DURATION = 10  # seconds
ZOMBIE_SPAWN_RATE = 2000  # milliseconds - slower spawning for better performance
MAX_ZOMBIES = 4  # fewer zombies on screen to reduce lag
POINTS_PER_HIT = 10
CLICK_COOLDOWN = 100  # milliseconds

# Zombie settings
ZOMBIE_SIZE = (120, 120)
ZOMBIE_LIFETIME_MIN = 1500  # milliseconds - shorter lifetime
ZOMBIE_LIFETIME_MAX = 3000  # milliseconds - shorter lifetime
ZOMBIE_HURT_DURATION = 200  # milliseconds
ZOMBIE_DEATH_TIMEOUT = 800  # milliseconds

# Audio settings
DEFAULT_MUSIC_VOLUME = 0.3
DEFAULT_SOUND_VOLUME = 0.5
VOLUME_STEP = 0.1
MIN_VOLUME = 0.0
MAX_VOLUME = 1.0

# Animation settings
ANIMATION_SPEED = 0.15
FRAME_LIMIT_IDLE = 6
FRAME_LIMIT_HURT = 3
FRAME_LIMIT_DYING = 8

# UI settings
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 100, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

class SoundType(Enum):
    CLICK = "click"
    HIT = "hit"
    MISS = "miss"
