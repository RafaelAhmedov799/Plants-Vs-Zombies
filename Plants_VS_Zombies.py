import random

import arcade

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from plants import Sunflower, PeaShooter, Nut, Tree
from zombies import OrdinaryZombie, ConeHeadZombie, BuckHeadZombie
import time

SCREEN_TITLE = "Plants VS Zombies"
MENU_WIDTH = 127


def cell_cx(x):
    if 236 < x < 335:
        return 0, (235+335)/2
    if 335 < x < 410:
        return 1, (335+410)/2
    if 410 < x < 500:
        return 2, (410+500)/2
    if 500 < x < 576:
        return 3, (500+576)/2
    if 576 < x < 665:
        return 4, (576+665)/2
    if 665 < x < 740:
        return 5, (665+740)/2
    if 740 < x < 820:
        return 6, (740+820)/2
    if 820 < x < 900:
        return 7, (820+900)/2
    if 900 < x < 970:
        return 8, (900+970)/2
    return 0, x


def cell_cy(y):
    if 26 < y < 130:
        return 0, (26+130)/2
    if 130 < y < 215:
        return 1, (130 + 215) / 2
    if 215 < y < 325:
        return 2, (215 + 325) / 2
    if 325 < y < 423:
        return 3, (325 + 423) / 2
    if 423 < y < 520:
        return 4, (423 + 520) / 2
    return 0, y


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bg = arcade.load_texture("textures/background.jpg")
        self.menu_texture = arcade.load_texture("textures/menu_vertical.png")
        self.cords = ""
        self.plants = arcade.SpriteList()
        self.seed = None
        self.taken_cells = []
        self.sun_money = 300
        self.bg_music = arcade.load_sound("sounds/grasswalk.mp3")
        self.seed_music = arcade.load_sound("sounds/seed.mp3")
        self.suns = arcade.SpriteList()
        self.peas = arcade.SpriteList()
        self.zombies = arcade.SpriteList()
        self.last_zombie_spawn_time = time.time()
        self.game = True
        self.killed_zombies = 0
        self.won = False
        self.win_texture = arcade.load_texture("textures/logo.png")
        self.hit_sound = arcade.load_sound("sounds/hit.mp3")
        self.peaspawn_sound = arcade.load_sound("sounds/peaspawn.mp3")
        self.sunspawn_sound = arcade.load_sound("sounds/sunspawn.mp3")
        self.lost = False
        self.end_texture = arcade.load_texture("textures/end.png")

    def setup(self):
        arcade.play_sound(self.bg_music, 0.3)

    def on_draw(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        arcade.draw_texture_rectangle(MENU_WIDTH/2, SCREEN_HEIGHT/2, MENU_WIDTH, SCREEN_HEIGHT, self.menu_texture)
        arcade.draw_text(self.cords, SCREEN_WIDTH, 0,arcade.color.BLACK, anchor_y = "bottom", anchor_x = "right")
        arcade.draw_text(f"{self.sun_money}", 60, 507, arcade.color.BROWN, 30,anchor_y="center", anchor_x="center")
        self.plants.draw()
        self.suns.draw()
        self.peas.draw()
        self.zombies.draw()
        if self.lost:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                              self.end_texture)
        if not self.game:
            if self.won:
                arcade.draw_rectangle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.color.BLACK)
                arcade.draw_texture_rectangle(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                              self.win_texture)
        if self.seed != None:
            self.seed.draw()

    def update(self, delta_time):
        if self.game:
            self.plants.update()
            self.plants.update_animation()
            self.suns.update()
            self.peas.update()
            self.zombies.update()
            self.zombies.update_animation()
            if time.time() - self.last_zombie_spawn_time > 5:
                row, center_y = cell_cy(random.randint(27, 519))
                zombie_type = random.randint(1, 3)
                if zombie_type == 1:
                    self.zombies.append(OrdinaryZombie(center_y, row, self))
                if zombie_type == 2:
                    self.zombies.append(ConeHeadZombie(center_y, row, self))
                if zombie_type == 3:
                    self.zombies.append(BuckHeadZombie(center_y, row, self))
                self.last_zombie_spawn_time = time.time()
            if self.killed_zombies >= 3:
                self.won = True
                self.game = False

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if 13 < x < 108:
            arcade.play_sound(self.seed_music, 0.5)
            if 370 < y < 480:
                self.seed = Sunflower(self)
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 200
            if 260 < y < 366:
                self.seed = PeaShooter(self)
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 200
            if 145 < y < 251:
                self.seed = Nut(self)
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 200
            if 30 < y < 145:
                self.seed = Tree(self)
                self.seed.center_x = x
                self.seed.center_y = y
                self.seed.alpha = 200

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.cords = f"{x},{y}"
        if self.seed != None:
            self.seed.center_x = x
            self.seed.center_y = y

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        for sun in self.suns:
            if sun.left < x < sun.right and sun.bottom < y < sun.top:
                self.sun_money += 25
                sun.kill()
        if self.seed == None:
            return
        if 40 < y < 520 and 250 < x < 970:
            c, cx = cell_cx(x)
            r, cy = cell_cy(y)
            if [r, c] not in self.taken_cells:
                if self.sun_money >= self.seed.cost:
                    self.sun_money -= self.seed.cost
                    self.taken_cells.append([r, c])
                    self.seed.place(cx, cy, r, c)
                    self.seed.alpha = 255
                    self.plants.append(self.seed)
                    self.seed = None
                    arcade.play_sound(self.seed_music, 0.5)
                else:
                    self.seed = None


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()