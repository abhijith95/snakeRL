from render import gameWindow
import pyglet
from pyglet.window import key

game = gameWindow(20,50,800,800,caption = "Snake!",resizable = True)
pyglet.clock.schedule_interval(game.update, 0.1)
pyglet.app.run() # command to execute running the window