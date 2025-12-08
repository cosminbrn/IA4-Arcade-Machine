# General idea 

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


