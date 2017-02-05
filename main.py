#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window


class FlappyBird(Widget):

    v = NumericProperty(0)
    g = -0.2

    def move(self):
        self.pos = Vector(0, self.v) + self.pos
        self.v += self.g


class FlappyBirdGame(Widget):

    bird = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlappyBirdGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def update(self, dt):
        if self.bird.y < 20:
            self.bird.v *= -0.3
            self.bird.y = 20
        if self.bird.top > self.height:
            self.bird.v *= -1
            self.bird.top = self.height
        self.bird.move()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, *args):
        if args[1][1] == 'w':
            if self.bird.v < 0:
                self.bird.v = 5
            else:
                self.bird.v += 0.5
        return True


class FlappyBirdApp(App):

    def build(self):
        game = FlappyBirdGame()
        Clock.schedule_interval(game.update, 1 / 60.0)
        return game

if __name__ == '__main__':
    FlappyBirdApp().run()
