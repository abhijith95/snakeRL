from render import gameWindow
import pyglet
from pyglet.window import key

gridSize = 20
noOfLevels = 90
game = gameWindow(gridSize,noOfLevels,800,800,caption = "Snake!",resizable = True)
pyglet.clock.schedule_interval(game.update, 0.01)
pyglet.app.run() # command to execute running the window