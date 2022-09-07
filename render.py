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
        self.game_Over = False
    
    def on_draw(self):
        self.clear()
        ctr = int(0)
        if self.game_Over:
            text = pyglet.text.Label("Game over", x = 500,y=700)
            text.draw()
        elif self.levelCtr>=self.maxLevel:
            text = pyglet.text.Label("Max level reached!", x = 500,y=700)
            text.draw()
        else:
            for i in range(self.gridSize):
                # i will change the y position
                for j in range(self.gridSize):
                    # j will change the x position
                    tile = pyglet.shapes.Rectangle(x = (self.startX + int(1*j*self.tileSize)),
                                                y = (self.startY - int(1*i*self.tileSize)),
                                                width = self.tileSize, height= self.tileSize,
                                                color = self.grid[ctr].color)
                    tile.draw()
                    # valueLabel = pyglet.text.Label(str(self.q[ctr,0]), font_size=6, color = (0,0,0,1),
                    #                                x = (self.startX + int(1*j*self.tileSize)) + (self.tileSize*0.5),
                    #                                y = (self.startY - int(1*i*self.tileSize)) + (self.tileSize*0.5),
                    #                                anchor_x='center',anchor_y='center')
                    # valueLabel.draw()
                    ctr+=1
                
    
    def update(self,dt):
        if self.levelCtr < self.maxLevel:
            self.game_Over,gameLevelUp = self.algorithm()
            if gameLevelUp:
                self.levelCtr+=1
            elif self.game_Over:
                print("Game over, agent lost")
                self.levelCtr = self.maxLevel +1
