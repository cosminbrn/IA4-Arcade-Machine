# Brick Invaders

Brick Invaders is a retro-inspired arcade shooter game, part of the LEGO Arcade Machine project.  
This folder contains all the code and assets for the Brick Invaders game.

## Folder Structure

brickinvaders/
│
├── __init__.py           # Package initialization
├── bullet.py             # Bullet sprite class and logic
├── constants.py          # Game-wide constants and image loading
├── explosion.py          # Explosion animation class
├── game.py               # Main game loop and state management
├── invader.py            # Invader sprite class and logic
├── score.py              # Score management and display
├── spaceship.py          # Spaceship sprite class and logic
├── utilities.py          # Helper functions for animation, collisions, etc.
└── README.md             # This documentation

## Main Modules and Classes

### `game.py`
**Brickinvaders**  
Main class for running the Brick Invaders game.  
Handles game state, event processing, updating, and rendering.

- **Some of the Attributes:**
  - `screen`: The game display surface.
  - `glb`: Global settings and state.
  - `score`: Score management object.
  - `dead`: Whether the player is dead.
  - `start_ticks`: Time when the game started (ms).
  - `images`: Store the images needed for the game.
  - `global_direction`: Variable that dictates the direction of the invaders and how much they advance once they reach the end of the screen.
  - `level_index`: Current level (also used in choosing which planet to blit)

- **Key Methods:**
  - `handle_event(event)`: Handles a single pygame event, such as pressing spacebar (shooting) and pressing the ESC key (leaving the game early)
  - `update()`: Updates game state and draws the frame.
  - `show_death_screen()`: Displays the death/game over screen.
  - `show_win_screen()`: Displays the win screen.
  - `check_functions()`: 4 functions that check for different types of collisions in the game (spaceship vs bullet, spaceship vs invader, invader vs bullet, invader vs bottom edge)
  - Most of these functions are explained below in the utilities.py section

---

### `bullet.py`
**Bullet**  
Represents a bullet fired by the player or an enemy.

- **Constructor Arguments:**
  - `x`, `y`: Initial position.
  - `image`: Bullet image.
  - `speed`: Bullet speed.
  - `angle`: Angle of movement in degrees.
  - `color`: Bullet color.

- **Key Methods:**
  - `update(score)`: Updates the bullet's position and checks if it is off-screen, also adds points

---

### `invader.py`
**Invader**  
Represents an enemy invader in the game.

- **Constructor Arguments:**
  - `x`, `y`: Initial position
  - `spritesheet`, `starting_frame`: The spritesheet for the invader and the starting frame of the spritesheet
  - `speed`, `shooting_change`: Speed and shooting chance variable that depend on what row, column or level the invader is in.
  - `enemy_bullet_image`, `enemy_bullets`: Sprite group for the enemy bullets and different colored bullets for each invader are possible thanks to these arguments.
  - `movement_multiplier`: How much space between invaders is allocated depends on this argument.

- **Key Methods:**
  - `update(direction, animation_func)`: Moves the invader and updates its animation frame, also handles the chance based shooting.
  
---

### `spaceship.py`
**Spaceship**  
Represents the player's spaceship.

- **Key Methods:**
  - `update()`: Updates the spaceship's position and handles input.
  - `draw()`: Draws the spaceship.

---

### `score.py`
**Score**  
Manages the player's score, streaks, and bonus logic.

- **Key Methods:**
  - `add_points(points)`: Adds points to the score.
  - `close_call()`: Awards points for close calls.
  - `reset()`: Resets the score and streaks.
  - `draw(screen, font, pos)`: Draws the score on the screen.
  - `add_combo(self)`: Adds combo points based on how many shots the user hit in a row.
  - `add_missed(self)`: Subtracts points based on how many shots the user missed.

---

### `constants.py`
Defines constants and the image loading function for Brick Invaders.

- **Key Constants:**
  - `SCREEN_WIDTH`, `SCREEN_HEIGHT`, `FPS`: Screen and timing settings.
  - `PLANET_FRAME_WIDTH`, `PLANET_FRAME_HEIGHT`, etc.: Spritesheet frame sizes.
  - `SPACESHIP_SPEED`: Speed of the player's spaceship.
  - `LEVELS`: List that contains the 10 unique levels.

- **Key Function:**
  - `load_images()`: Loads and returns all images and spritesheets used in the game.

---

### `utilities.py`
Helper functions for Brick Invaders.

- **Key Functions:**
  - `show_win_screen(self)`: Display the win screen and handle bonus logic.
  - `show_death_screen(self)`: Display the death/game over screen.
  - `planet_animation(self, planet_index, spritesheet_index)`: Animate planet backgrounds.
  - `spaceship_animation(self, spritesheet, spritesheet_index)`: Animate the spaceship.
  - `invader_animation(self, spritesheet, spritesheet_index)`: Animate invaders.
  - `explosion_animation(self, spritesheet, x, y)`: Animate explosions.
  - `setup_level(self, level_data)`: Set up a new level based on the attributes saved in the LEVELS list explained previously.
  - `check_bullet_invader_collisions(self)`: Handle bullet/invader collisions.
  - `check_enemy_bullet_spaceship_collisions(self)`: Handle enemy bullet/spaceship collisions. Also shrinks the spaceship's hitbox for easier difficulty and adds close call points when a bullet passes right by the hitbox.
  - `check_invaders_reach_bottom(self)`: End game if invaders reach the bottom.
  - `check_invader_spaceship_collisions(self)`: Handle invader/spaceship collisions.
  - `animation(self)`: Smoothly animates the spaceship moving to the center, then scrolls the background and planet to transition to the next level. The planet and background scroll with easing effects, and the spaceship's angle is smoothly reset. The function also updates the planet offset if the next level uses a special background (galaxy, star, blackhole).

---

## How the Game Works

- The game initializes all assets and displays a loading animation.
- The player controls a spaceship, shooting at waves of invaders.
- The score system rewards accuracy, streaks, and close calls.
- The game ends if the player is hit or if invaders reach the bottom.
- A win screen is shown if all levels are completed.

---