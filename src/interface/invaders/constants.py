import pygame
# constants for Brick Invaders game

# screen settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# animation settings
PLANET_OFFSET_X = -1000 # lower is left
PLANET_OFFSET_Y = 400 # lower is higher

GALAXY_OFFSET_X = -750
GALAXY_OFFSET_Y = -100 

STAR_OFFSET_X = -900
STAR_OFFSET_Y = 100

# FIX BLACKHOLE Y OFFSET
BLACKHOLE_OFFSET_X = -250
BLACKHOLE_OFFSET_Y = 350

PLANET_ANIMATION_SLOWDOWN = 700  # higher is slower
PLANET_FRAME_WIDTH = 240
PLANET_FRAME_HEIGHT = 240
PLANET_SPRITESHEET_COLUMNS = 6
PLANET_SPRITESHEET_ROWS = 6
PLANET_TOTAL_FRAMES = PLANET_SPRITESHEET_COLUMNS * PLANET_SPRITESHEET_ROWS

# spaceship settings
SPACESHIP_SPEED = 10
SPACESHIP_ACCELERATION = 0.6
SPACESHIP_FRICTION = 0.4
SPACESHIP_VELOCITY_LIMIT = 15
SPACESHIP_COUNTER_STRAFE_MULTIPLIER = 2
SPACESHIP_ANGLE_INCREMENT = 5
SPACESHIP_FRAME_WIDTH = 48
SPACESHIP_FRAME_HEIGHT = 48
SPACESHIP_SPRITESHEET_COLUMNS = 2
SPACESHIP_SPRITESHEET_ROWS = 2
SPACESHIP_TOTAL_FRAMES = SPACESHIP_SPRITESHEET_COLUMNS * SPACESHIP_SPRITESHEET_ROWS
SPACESHIP_ANIMATION_SLOWDOWN = 200 # higher is slower

# bullet settings
BULLET_SPEED = 25
BULLET_WIDTH = 16
BULLET_HEIGHT = 16

# invader settings
INVADER_ROWS = 5
INVADER_COLUMNS = 11
INVADER_START_X = 200
INVADER_START_Y = 50
INVADER_SPEED = 2
INVADER_DOWN = 25
INVADER_WIDTH = SCREEN_WIDTH // 25
INVADER_HEIGHT = SCREEN_HEIGHT // 17
INVADER_SPRITESHEETS = 5
INVADER_FRAME_WIDTH = 48
INVADER_FRAME_HEIGHT = 48
INVADER_SPRITESHEET_COLUMNS = 2
INVADER_SPRITESHEET_ROWS = 2
INVADER_TOTAL_FRAMES = INVADER_SPRITESHEET_COLUMNS * INVADER_SPRITESHEET_ROWS
INVADER_ANIMATION_SLOWDOWN = 500  # higher is slower
INVADER_BULLET_SPEED = 5
INVADER_BULLET_WIDTH = 24
INVADER_BULLET_HEIGHT = 24

# explosion settings
EXPLOSION_WIDTH = INVADER_WIDTH
EXPLOSION_HEIGHT = INVADER_HEIGHT
EXPLOSION_FRAME_WIDTH = INVADER_FRAME_WIDTH
EXPLOSION_FRAME_HEIGHT = INVADER_FRAME_HEIGHT
EXPLOSION_SPRITESHEET_COLUMNS = 2
EXPLOSION_SPRITESHEET_ROWS = 2
EXPLOSION_TOTAL_FRAMES = EXPLOSION_SPRITESHEET_COLUMNS * EXPLOSION_SPRITESHEET_ROWS
EXPLOSION_ANIMATION_SLOWDOWN = 500

# scoring
CLOSE_CALL_POINTS = 50
INVADER_DESTROYED_POINTS = 100
MISSED_PENALTY = 25
COMBO_BASE_SCORE = 10

def load_images():
    bullet_image = pygame.transform.rotate(
        pygame.image.load('./assets/invaders/spaceship_bullet.png').convert_alpha(),
        180
    )
    planets = [
        pygame.image.load('./assets/invaders/planet1_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet2_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet3_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet4_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet5_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet6_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/planet7_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/galaxy_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/star_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/blackhole_spritesheet.png').convert_alpha()
    ]
    spaceship_spritesheet = pygame.image.load('./assets/invaders/spaceship_spritesheet.png').convert_alpha()
    invaders = [
        pygame.image.load('./assets/invaders/invader1_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/invader2_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/invader3_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/invader4_spritesheet.png').convert_alpha(),
        pygame.image.load('./assets/invaders/invader5_spritesheet.png').convert_alpha()
    ]
    explosion = pygame.image.load('./assets/invaders/explosion_spritesheet.png').convert_alpha()
    enemy_bullet_image = pygame.transform.scale(
        pygame.image.load('./assets/invaders/invader_bullet.png').convert_alpha(),
        (INVADER_BULLET_WIDTH, INVADER_BULLET_HEIGHT)
    )
    return bullet_image, planets, spaceship_spritesheet, invaders, explosion, enemy_bullet_image

# level definitions
LEVELS = [
    { 
        "rows": 5, #5 
        "columns": 9,
        "invader_speed": 1.5,
        "pattern": "default",
        "shooting_chance": 0.0005,
        "spacing_multiplier": 1.8 # good first level
    },
    {
        "rows": 5, #5
        "columns": 9,
        "invader_speed": 3,
        "pattern": "zigzag",
        "shooting_chance": 0.00005,
        "spacing_multiplier": 1.8
    },
    {
        "rows": 6, #6
        "columns": 13,
        "invader_speed": 1.2,
        "pattern": "dense",
        "shooting_chance": 0,
        "spacing_multiplier": 1.5
    },
    {
        "rows": 5, #
        "columns": 11,
        "invader_speed": 0,
        "pattern": "M",
        "shooting_chance": 0.0015,
        "spacing_multiplier": 2
    },
    {
        "rows": 8, #6
        "columns": 14,
        "invader_speed": 2.8,
        "pattern": "checker",
        "shooting_chance": 0.000075,
        "spacing_multiplier": 1.2
    },
    {
        "rows": 6, #6
        "columns": 11,
        "invader_speed": 3.4,
        "pattern": "default",
        "shooting_chance": None,
        "spacing_multiplier": 1.55
    },
    {
        "rows": 10, #10
        "columns": 18,
        "invader_speed": 0.5,
        "pattern": "wall",
        "shooting_chance": 0.0003,
        "spacing_multiplier": 1.1
    },
    {
        "rows": 12,
        "columns": 18,
        "invader_speed": 1.5,
        "pattern": "reversetriangle",
        "shooting_chance": 0.0005,
        "spacing_multiplier": 1.2
    },
    {
        "rows": 6, #6
        "columns": 12,
        "invader_speed": 3.0,
        "pattern": "wave",
        "shooting_chance": 0.000005,
        "spacing_multiplier": 1.4
    },
    {
        "rows": 12, #12
        "columns": 16,
        "invader_speed": 0.125,
        "pattern": "onslaught",
        "shooting_chance": 0.0125,
        "spacing_multiplier": 1.05
    }
]