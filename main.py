#!/usr/bin/env python

import kivyconfig
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint

w_height = 600
w_width = 800
Window.size = (w_width, w_height)


class FlappyBird(Widget):

    """Flappy bird class

    Attributes:
        v: vertical upward velocity of the bird.
        g: gravity of the bird
        score: score of the bird
    """

    v = NumericProperty(0)
    g = -0.2  # static constant
    score = NumericProperty(0)

    def move(self):
        """Update position according to velocity and update velocity according to gravity"""
        self.pos = Vector(0, self.v) + self.pos
        self.v += FlappyBird.g


class Obstacle(Widget):

    """Vertical obstacle class

    Attributes:
        bot_hol: y coordinate of the hole bottom
        top_hol: y coordinate of the hole top
        wide: width of the obstacle
        v: horizontal velocity of the obstacle
        acceleration: acceleration of the obstacle
        state: 1 - bird inside the hole, 0 - otherwise

         wide
        <--->
        _____  <--- window height (y = 600)
        |   |
        |   |
        |   |
        -----  <--- top_hol (150 <= y - bot_hol <= 200) \
                                                         >--- hole size in range(150, 200 + 1)
        _____  <--- bot_hol (120 <= y <= 400)           /
        |   |
        |   |
        |   |
    ------------- <-- platform (y = 20)
    -------------

    """

    # hole parameters
    bot_hol = NumericProperty(0)
    top_hol = NumericProperty(0)
    # other physical parameters
    wide = NumericProperty(100)
    v = NumericProperty(6)
    acceleration = 0.001  # static constant

    state = 0

    def __init__(self, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        # hole parameters are created at the instantiation
        self.make_hole()

    def move(self):
        self.pos = Vector(-self.v, 0) + self.pos
        # acceleration
        self.v += Obstacle.acceleration
        # if disappears from left, appear from right side
        if self.right < 0:
            self.pos = Vector(w_width, 0)
            # with a different hole
            self.make_hole()

    def follow(self, obstacle, offset):
        """Follow another widget(= obstacle) keeping a distance

        Args:
            obstacle: widget to be followed
            offset: distance offset from the obstacle
        """
        # keeps the same acceleration
        self.v += Obstacle.acceleration
        self.pos = Vector(offset, 0) + obstacle.pos

    def make_hole(self):
        """Make a new hole with randoms for position and size with the given constraints"""
        self.bot_hol = randint(20 + 100, w_height - 200)
        self.top_hol = randint(150, 200) + self.bot_hol


class FlappyBirdGame(Widget):

    """Flappy Bird game class

    Attributes:
        bird: flappy bird
        obstacle1: obstacle 1
        obstacle2: obstacle 2
    """

    bird = ObjectProperty(None)
    obstacle1 = ObjectProperty(None)
    obstacle2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FlappyBirdGame, self).__init__(**kwargs)
        # keyboard configuration
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def update(self, dt):
        """Call at regular time intervals ie. frame rate"""
        # check collision and update score accordingly
        self.check_collision(self.obstacle1)
        self.check_collision(self.obstacle2)
        # if bird falls on platform, bounce with 0.3 times the velocity
        if self.bird.y < 20:
            self.bird.v *= -0.3
            self.bird.y = 20
        # if bird reaches the top, block it
        if self.bird.top > self.height:
            self.bird.v *= -1
            self.bird.top = self.height
        # make the obstacle1 move
        self.obstacle1.move()
        # as the obstacle2 comes following the obstacle1, obstacle2.follow() is called. But if obstacle1 appears from
        #   right side, obstacle2 stops following obstacle1 and starts obstacle2.move().
        if self.obstacle1.x < self.obstacle2.x:
            self.obstacle2.follow(self.obstacle1, w_width / 2 + self.obstacle2.width / 2)
        else:
            self.obstacle2.move()
        # move the bird
        self.bird.move()

    def check_collision(self, obstacle):
        """Check collision with the bird and the obstacle and update score accordingly

         Args:
             obstacle: widget to be checked for collision
        """

        # if the bird in the danger zone
        if self.bird.right > obstacle.x and \
                self.bird.x < obstacle.x + obstacle.width and \
                (self.bird.top < obstacle.top_hol and -self.bird.height + self.bird.top > obstacle.bot_hol):
            if obstacle.state == 0:
                self.bird.score += 1
            obstacle.state = 1
        else:
            obstacle.state = 0
        # if the bird in the hole
        if self.bird.right > obstacle.x and \
                self.bird.x < obstacle.x + obstacle.width and \
                (self.bird.top > obstacle.top_hol or -self.bird.height + self.bird.top < obstacle.bot_hol):
            self.bird.score -= 0.1

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
