import pygame

class Menu:
    name = "Menu"
    new_game = "None"
    running = True
    up = True
    left = True
    selected_item = 0   # 0 to 3 values (inclusive)

    def __init__(self, new_screen, new_globals):
        self.screen = new_screen
        self.glb = new_globals
        # self.background = pygame.image.load("././assets/menu/images/bg.png")
        # self.background = pygame.transform.scale(self.background, (self.glb.WINWIDTH, self.glb.WINHEIGHT))

    def controls(self):
        keys = pygame.key.get_pressed()
        state = {
            'w': keys[pygame.K_w],
            'a': keys[pygame.K_a],
            's': keys[pygame.K_s],
            'd': keys[pygame.K_d],
            'space': keys[pygame.K_SPACE]
        }
        
        if state['w']:
            self.up = True
        if state['a']:
            self.left = True
        if state['s']:
            self.up = False
        if state['d']:
            self.left = False

        if self.up and self.left:
            self.selected_item = 0
        elif self.up and not self.left:
            self.selected_item = 1
        elif not self.up and self.left:
            self.selected_item = 2
        elif not self.up and not self.left:
            self.selected_item = 3

        if state['space']:
            self.change_game()

    def change_game(self):
        match self.selected_item:
            case 0:
                self.new_game = "Invaders"
            case 1:
                self.new_game = "DontTouchMyPresents"
            case 2:
                pass
        
        print("Changing game to " + self.new_game + "...")
        self.running = False

    def update(self):
        if not self.screen:
            print("No screen at Menu.update()... Check for errors.")
            return
        
        # if not self.background:
        #     print("Background not loaded at Menu.update()... Check for errors.")
        #     return
        
        if not self.glb:
            print("Global parameters not loaded at Menu.update()... Check for errors.")
        
        selected_color = (255, 150, 0) # orangey colour
        unselected_color = (50, 50, 50) # grey
        grid_item_height = 270
        grid_item_width = 480
        padding_size_horz = 300
        padding_size_vert = padding_size_horz * 0.55

        game_positions = [
            [(self.glb.WINWIDTH - padding_size_horz) / 2 - grid_item_width, (self.glb.WINHEIGHT - padding_size_vert) / 2 - grid_item_height],
            [(self.glb.WINWIDTH + padding_size_horz) / 2, (self.glb.WINHEIGHT - padding_size_vert) / 2 - grid_item_height],
            [(self.glb.WINWIDTH - padding_size_horz) / 2 - grid_item_width, (self.glb.WINHEIGHT + padding_size_vert) / 2],
            [(self.glb.WINWIDTH + padding_size_horz) / 2, (self.glb.WINHEIGHT + padding_size_vert) / 2]
        ]
        
        # self.screen.blit(self.background, (0, 0))

        for i in range(0, 3):
            color = selected_color if self.selected_item == i else unselected_color
            pygame.draw.rect(self.screen, color, pygame.Rect(game_positions[i][0], game_positions[i][1], grid_item_width, grid_item_height))

        pygame.display.update()
        self.controls()