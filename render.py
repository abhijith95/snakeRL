import pyglet
from pyglet.window import key
from agent import agent

class gameWindow(pyglet.window.Window,agent):
    
    def __init__(self,gridSize,maxGame,*args,**kwargs):
        agent.__init__(self,gridSize)
        pyglet.window.Window.__init__(self,*args,**kwargs)
        self.levelCtr = 0 # number of games played in total
        self.gridSize = gridSize
        self.startX, self.startY = 200,600
        self.tileSize = 20
        self.maxLevel = maxGame
    
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
        if self.levelCtr < self.maxLevel:
            game_Over,gameLevelUp = self.algorithm()
            if gameLevelUp:
                self.levelCtr+=1
            elif game_Over:
                print("Game over, agent lost")
                self.levelCtr = self.maxLevel +1
