#!/usr/bin/env python

import kivyconfig
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
from collections import deque

w_height = 600
w_width = 800
Window.size = (w_width, w_height)


class FlappyBird(Widget):

    v = NumericProperty(0)
    g = -0.2
    score = NumericProperty(0)

    def move(self):
        self.pos = Vector(0, self.v) + self.pos
        self.v += self.g


class Obstacle(Widget):

    bot_hol = NumericProperty(0)
    top_hol = NumericProperty(0)
    wide = NumericProperty(100)
    v = NumericProperty(6)
    acceleration = 0.001
    # 0 - none, 1 - bird inside
    state = 0

    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.make_hole()

    def move(self):
        self.pos = Vector(-self.v, 0) + self.pos
        self.v += Obstacle.acceleration
        if self.right < 0:
            self.pos = Vector(w_width, 0)
            self.make_hole()

    def follow(self, obstacle, offset=100):
        self.v += Obstacle.acceleration
        self.pos = Vector(offset, 0) + obstacle.pos

    def check_collide(self, bird):
        if bird.right > self.x and \
                bird.x < self.x + self.width and \
                (bird.top < self.top_hol and -bird.height + bird.top > self.bot_hol):
            if self.state == 0:
                bird.score += 1
            self.state = 1
        else:
            self.state = 0
        if bird.right > self.x and \
                bird.x < self.x + self.width and \
                (bird.top > self.top_hol or -bird.height + bird.top < self.bot_hol):
            bird.score -= 0.1

    def make_hole(self):
        self.bot_hol = randint(20 + 100, w_height - 200)
        self.top_hol = randint(150, 200) + self.bot_hol


class FlappyBirdGame(Widget):

    bird = ObjectProperty(None)
    obstacle1 = ObjectProperty(None)
    obstacle2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlappyBirdGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def update(self, dt):
        self.obstacle1.check_collide(self.bird)
        self.obstacle2.check_collide(self.bird)
        if self.bird.y < 20:
            self.bird.v *= -0.3
            self.bird.y = 20
        if self.bird.top > self.height:
            self.bird.v *= -1
            self.bird.top = self.height
        self.obstacle1.move()
        if self.obstacle1.x < self.obstacle2.x:
            self.obstacle2.follow(self.obstacle1, w_width / 2 + self.obstacle2.width / 2)
        else:
            self.obstacle2.move()
        # self.obstacle2.move()
        self.bird.move()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, *args):
        if args[1][1] == 'w':
            if self.bird.v < 5:
                self.bird.v = 6
            else:
                self.bird.v += 1
        return True


class FlappyBirdApp(App):

    def build(self):
        game = FlappyBirdGame()
        Clock.schedule_interval(game.update, 1 / 60.0)
        return game

if __name__ == '__main__':
    FlappyBirdApp().run()
