# IA4-Tetris-Project
3 in 1 game macnine

## Prerequisites and tehnologies used
- python ^3.10
- pip & pipx
- pygame (installed through pipx ```pipx install pygame```)
- make (for the Makefile)

## Scripts
- ```make run``` - install and run
- ```make install``` install only
- ```make uninstall``` uninstall project

## Running
- After installation, all is needed is to use the terminal to run the game using the
```sh
  interface
```

## What each of us did

- Each of us worked on his own personal game
- The logic and idea of the interface, as well as the code for it was a common idea that we all came up with.
- Pana Robert-Ionut is responsible for the Okey Card Game
- Chifan Eduard-Mario is responsible for the Don't Touch My Presents Game
- Baroana Cosmin-George is responsible for the Invaders Game

## Repo Link
- https://github.com/cosminbrn/IA4-Arcade-Machine

# Gambling General idea 

Welcome to the **Okey Card Minigame**. A faithful recreation of the Metin2 Okey Event. With authentic textures and classic interface design, this game aims to bring back the nostalgia of the game that defined our childhoods.

- Built using **Pygame**.

- Implements several design patterns

- Designed in a classic, arcade-like way
---
The ``assets package``  contains the textures for all the cards, placeholders and images used in the game.

The *commands.py* module implements the command design pattern for actions in the game. Briefly said, it converts requests to operations on different objects. 

The *observers.py* module implements the Observer Pattern. It provides a way to react to events happening in other objects without coupling classes.

The *models.py* module implements the internal logic for the Card class, the Deck of cards class. The actions of drawing, making combo's, discarding cards, moving cards from the deck to the playing hand and calculating the points.

The *animation_manager.py* module implements the animations for drawing, moving and combining cards and for resetting the game.

The *view.py* module handles the GUI. It is responsible for drawing all visual elements and manages the rendering logic of the game. It processes user input by translating mouse clicks into executable game commands.

The *resource_manager.py* module handles the loading and management of game assets and fonts.


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


# 🎁 Don't Touch My Presents

**Don't Touch My Presents** is a fast-paced, mouse-based arcade 
mini-game included as part of the Arcade Machine project. 
The player's objective is to defend the main present from thieving 
hands that attempt to grab it, by moving the present with the mouse 
to avoid contact.

The game rewards quick reflexes and accuracy, with difficulty 
increasing as the hands' speed accelerates.

## 📁 Folder Structure

presents/
│
├── constants.py          # Game constants, scaling settings, and asset paths.
├── flake.py              # Class for the individual snowflakes (visual background effect).
├── game.py               # Main game logic (menu screen, gameplay, game over).
├── hand.py               # Class for the enemy hands.
├── scoreboard.py         # Class for score management and display.
└── README.md             # This documentation


## 💻 Main Modules and Classes

### `game.py` - Class `DontTouchMyPresents`

This is the **main class** of the game. It manages the game loop, 
game state (`"menu"`, `"game"`, `"gameover"`), asset loading, and general 
interaction (input, collisions, transitions).

* **Key Attributes:**
    * `game_surface`: The centralized game drawing surface.
    * `gamestate`: The current state of the game.
    * `present_rect`: The `pygame.Rect` object for the gift, 
        controlled by the player.
    * `hands`: List of `HandGame` objects.
    * `dragging_present`: Flag to track if the player is currently 
        dragging the present.
* **Key Methods:**
    * `reset_game_session()`: Sets up the game state for a new session.
    * `handle_event(event)`: Processes mouse events (click, motion) to 
        enable dragging the present and interacting with buttons.
    * `update()`: Updates game logic (hand movement, present-hand 
        collision checks) and renders the frame.

### `hand.py` - Class `HandGame`

Represents an enemy hand that descends to steal the present.

* **Mechanics:** Hands appear from the top of the screen (left and right) 
    with a speed that gradually increases throughout the game.
* **Key Methods:**
    * `reset()`: Resets the hand to the top of the screen, off-screen, 
        and resets the `passed_present` flag.
    * `update()`: Updates the hand's Y-position. **Accelerates** the speed 
        over time (`HAND_ACCEL`) and resets the hand when it reaches the 
        bottom of the screen.

### `scoreboard.py` - Class `ScoreBoard`

Manages the player's score.

* **Scoring Logic:** The score increments by **+1** (`add_score()`) when 
    a hand successfully passes the present without a collision.

### `flake.py` - Class `Flake`

Handles the logic for individual snowflakes, creating a visual snowing 
effect in the background.

* **Key Methods:**
    * `update()`: Moves the snowflake down and resets it to the top when 
        it exits the screen.

### `constants.py`

Defines essential configuration variables.

* **Key Constants:**
    * `SCALE`: Scaling factor based on the target resolution.
    * `GAME_W`, `GAME_H`: Dimensions of the game surface.
    * `HAND_START_SPEED`, `HAND_MAX_SPEED`, `HAND_ACCEL`: Parameters 
        controlling hand movement and difficulty scaling.

---

## 🎮 How to Play

1.  **Main Menu:** The game starts on the menu screen with the snowing 
    background. Click **"Start Game"**.
2.  **Gameplay:**
    * The player **drags and moves** the present (`present_rect`) 
        using the mouse.
    * Enemy hands (`HandGame`) begin descending from the top after a 
        short initial delay.
    * **Goal:** Avoid collision with the hands for as long as possible.
    * **Scoring:** Points are awarded when a hand successfully **passes 
        the present** without touching it.
3.  **Game Over:** The game ends immediately when the present **collides** with any of the descending hands.
4.  **Game Over Screen:** Displays the final score and offers options to 
    **"Restart"** or **"Return to Menu"**.
