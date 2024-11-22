import arcade

from Level_2.animated import Animated

from constants import SCREEN_WIDTH


class Zombie(Animated):
    def __init__(self, file_name, health, row, center_y, window):
        super().__init__(file_name, 0.09)
        self.health = health
        self.row = row
        self.center_y = center_y
        self.change_x = -0.2
        self.left = SCREEN_WIDTH
        self.window = window

    def update(self):
        super().update()
        if self.health <= 0:
            self.window.killed_zombies += 1
            self.kill()
        plants = arcade.check_for_collision_with_list(self, self.window.plants)
        eating = False
        for plant in plants:
            if self.row == plant.row:
                eating = True
                plant.health -= 0.5
        if eating:
            self.change_x = 0
            self.angle = 15
        else:
            self.change_x = -0.2
            self.angle = 0
        if self.left <= 200:
            self.window.game = False
            self.window.lost = True


class OrdinaryZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__("zombies/zom1.png", 12, row, center_y, window)
        self.append_texture(arcade.load_texture("zombies/zom1.png"))
        self.append_texture(arcade.load_texture("zombies/zom2.png"))
        self.append_texture(arcade.load_texture("zombies/zom2.png"))


class ConeHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__("zombies/cone1.png", 20, row, center_y, window)
        self.append_texture(arcade.load_texture("zombies/cone1.png"))
        self.append_texture(arcade.load_texture("zombies/cone2.png"))
        self.append_texture(arcade.load_texture("zombies/cone2.png"))


class BuckHeadZombie(Zombie):
    def __init__(self, center_y, row, window):
        super().__init__("zombies/buck1.png", 32, row, center_y, window)
        self.append_texture(arcade.load_texture("zombies/buck1.png"))
        self.append_texture(arcade.load_texture("zombies/buck2.png"))
        self.append_texture(arcade.load_texture("zombies/buck2.png"))



