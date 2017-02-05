#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class FlappyBird(Widget):

    v = NumericProperty(0)
    g = -0.2

    def move(self):
        self.pos = Vector(0, self.v) + self.pos
        self.v += self.g


class FlappyBirdGame(Widget):

    bird = ObjectProperty(None)

    def update(self, dt):
        if self.bird.y < 20:
            self.bird.v = 0
        self.bird.move()


class FlappyBirdApp(App):

    def build(self):
        game = FlappyBirdGame()
        Clock.schedule_interval(game.update, 1 / 60.0)
        return game

if __name__ == '__main__':
    FlappyBirdApp().run()