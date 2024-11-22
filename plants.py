import time

import arcade

from Level_2.animated import Animated


class Plant(Animated):
    def __init__(self, filename,health, cost, window):
        super().__init__(filename, 0.12)
        self.health = health
        self.cost = cost
        self.row = 0
        self.column = 0
        self.window = window

    def update(self):
        if self.health <= 0:
            self.window.taken_cells.remove([self.row, self.column])
            self.kill()

    def place(self, center_x, center_y, row, column):
        self.set_position(center_x, center_y)
        self.row = row
        self.column = column


class Sun(arcade.Sprite):
    def __init__(self, left, bottom):
        super().__init__("items/sun.png", 0.12)
        self.left = left
        self.bottom = bottom
        self.change_angle = 1
        self.creation_time = time.time()

    def update(self):
        super().update()
        if time.time() - self.creation_time > 3:
            self.kill()


class Sunflower(Plant):
    def __init__(self, window):
        super().__init__("plants/sun1.png", 80, 50, window)
        self.append_texture(arcade.load_texture("plants/sun1.png"))
        self.append_texture(arcade.load_texture("plants/sun2.png"))
        self.last_sun_spawn_time = time.time()

    def update(self):
        super().update()
        if time.time() - self.last_sun_spawn_time > 5:
            self.window.suns.append(Sun(self.right - 15, self.top - 15))
            self.last_sun_spawn_time = time.time()
            arcade.play_sound(self.window.sunspawn_sound, 1)


class Pea(arcade.Sprite):
    def __init__(self, left, bottom, window):
        super().__init__("items/bul.png", 0.12)
        self.left = left
        self.bottom = bottom
        self.change_x = 7
        self.window = window
        self.damage = 1
        self.win = 0

    def update(self):
        super().update()
        zombies = arcade.check_for_collision_with_list(self, self.window.zombies)
        for zombie in zombies:
            zombie.health -= self.damage
            arcade.play_sound(self.window.hit_sound, 1)

        if len(zombies) > 0:
            self.kill()


class PeaShooter(Plant):
    def __init__(self, window):
        super().__init__("plants/pea1.png", 80, 100, window)
        self.append_texture(arcade.load_texture("plants/pea2.png"))
        self.append_texture(arcade.load_texture("plants/pea3.png"))
        self.last_pea_spawn_time = time.time()

    def update(self):
        super().update()
        zombie_on_line = False
        for zombie in self.window.zombies:
            if zombie.row == self.row:
                zombie_on_line = True
        if time.time() - self.last_pea_spawn_time > 2 and zombie_on_line:
            self.window.peas.append(Pea(self.right, self.top - 30, self.window))
            self.last_pea_spawn_time = time.time()
            arcade.play_sound(self.window.peaspawn_sound, 1)


class Nut(Plant):
    def __init__(self, window):
        super().__init__("plants/nut1.png", 80, 50, window)
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut1.png"))
        self.append_texture(arcade.load_texture("plants/nut2.png"))
        self.append_texture(arcade.load_texture("plants/nut3.png"))


class Tree(Plant):
    def __init__(self, window):
        super().__init__("plants/tree1.png", 80, 175, window)
        self.append_texture(arcade.load_texture("plants/tree2.png"))
        self.append_texture(arcade.load_texture("plants/tree3.png"))

    def update(self):
        super().update()
        peas = arcade.check_for_collision_with_list(self, self.window.peas)
        for pea in peas:
            pea.texture = arcade.load_texture("items/firebul.png")
            pea.damage = 3
