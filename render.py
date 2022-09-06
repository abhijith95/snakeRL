import pyglet
from pyglet.window import key
from agent import agent

class gameWindow(pyglet.window.Window,agent):
    
    def __init__(self,gridSize,maxGame,*args,**kwargs):
        agent.__init__(self,gridSize)
        pyglet.window.Window.__init__(self,*args,**kwargs)
        self.gameCtr = 0 # number of games played in total
        self.gridSize = gridSize
        self.startX, self.startY = 200,600
        self.tileSize = 20
        self.maxGame = maxGame
    
    def on_draw(self):
        self.clear()
        ctr = int(0)
        for i in range(self.gridSize):
            # i will change the y position
            for j in range(self.gridSize):
                # j will change the x position
                tile = pyglet.shapes.Rectangle(x = (self.startX + int(1*j*self.tileSize)),
                                               y = (self.startY - int(1*i*self.tileSize)),
                                               width = self.tileSize, height= self.tileSize,
                                               color = self.grid[ctr].color)
                tile.draw()
                ctr+=1
                
    
    def update(self,dt):
        while self.gameCtr < self.maxGame:
            game_Over,gameLevelUp = self.algorithm()
            if gameLevelUp:
                self.gameCtr+=1
            elif game_Over:
                print("Game over, agent lost")
                self.gameCtr = self.maxGame +1


game = gameWindow(20,10,800,800,caption = "Snake!",resizable = True)
pyglet.clock.schedule_interval(game.update, 1)
pyglet.app.run() # command to execute running the window