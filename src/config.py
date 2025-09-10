SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

ASSET_DIR = "assets/"
IMG_DIR = ASSET_DIR + "images/"
SOUND_DIR = ASSET_DIR + "sounds/"
FONT_DIR = ASSET_DIR + "fonts/"

# Game settings
GAME_DURATION = 60  # seconds
ZOMBIE_SPAWN_RATE = 2000  # milliseconds - slower spawning for better performance
MAX_ZOMBIES = 4  # fewer zombies on screen to reduce lag
POINTS_PER_HIT = 10

# Zombie settings
ZOMBIE_SIZE = (120, 120)
ZOMBIE_LIFETIME_MIN = 1500  # milliseconds - shorter lifetime
ZOMBIE_LIFETIME_MAX = 3000  # milliseconds - shorter lifetime

# Audio settings
DEFAULT_MUSIC_VOLUME = 0.3
DEFAULT_SOUND_VOLUME = 0.5
VOLUME_STEP = 0.1
