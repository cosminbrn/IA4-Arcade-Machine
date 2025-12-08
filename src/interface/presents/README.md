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