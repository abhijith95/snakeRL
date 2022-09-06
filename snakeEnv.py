import random

class gridTile:
    # this class contains the information about each tile in the grid
    def __init__(self,id,isSnake,isApple,isNormal):
        self.id = id
        """
        Following parameters contains the information on the type of
        tile. Does the tile contain the snake body or the apple
        or is it part of the boundary or is it a normal tile?
        """
        self.isSnake = isSnake
        self.isApple = isApple
        self.isNormal = isNormal
        self.isWall = False
        
        # color of different tiles
        self.snakeTileColor = (0,255,0)
        self.appleTileColor = (255,0,0)
        self.tileColor = (255,255,255)
        
        self.defineTileColor()
    
    def defineTileColor(self):
        self.color = (self.isSnake*self.snakeTileColor) + \
                    self.isNormal*self.tileColor + self.isApple*self.appleTileColor

class snakeEnv:
    
    # the snake game shall be grid of size nxn.
    def __init__(self,gridSize):
        
        self.gridSize = gridSize
        self.grid = [] # initializing the grid for the game
        self.possibleActions = ['UP','DOWN',
                                'RIGHT','LEFT']
        self.gameReset()
        
        # in the beginning the snake will begin to move to the right
        self.currentAction = self.possibleActions[2]
        
        # action mapping of the head
        self.actionDict = {self.possibleActions[0]: {'VX':0,'VY':int(-self.gridSize)},
                           self.possibleActions[1]: {'VX':0,'VY':int(+self.gridSize)},
                           self.possibleActions[2]: {'VX':1,'VY':0},
                           self.possibleActions[3]: {'VX':-1,'VY':0}}
    
    def gameReset(self):
        # function that resets the game to level 1
        
        # id of the tiles that contains the snake body. This is fixed
        # relative to the grid size. Head will always be at the end of the list
        head = int(self.gridSize*self.gridSize/2) + int(self.gridSize/2)
        self.snake = [head-1, head] 
        ctr = 0
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                isNormal = True
                isApple = False # the apple will be randomly set after the for loop
                isSnake = False
                
                if ((ctr)== head) or ((ctr)==head-1):
                    isSnake = True  
                    isNormal = False
                temp = gridTile( id = ctr, isSnake= isSnake, isApple=isApple,
                                isNormal=isNormal)
                if (i==0) or (j== 0) or (i==self.gridSize-1) or (j==self.gridSize-1):
                    temp.isWall = True
                self.grid.append(temp)
                ctr+=1     
        self.resetApple()
    
    def resetApple(self):
        # sets the position of the apple in the grid
        self.appleId = self.snake[0]
        while self.appleId in self.snake:
            self.appleId = random.randint(0,self.gridSize*self.gridSize-1)
            if self.appleId not in self.snake:
                self.grid[self.appleId].isNormal = False
                self.grid[self.appleId].isSnake = False
                self.grid[self.appleId].isApple = True
                self.grid[self.appleId].defineTileColor()
                break
    
    def getVelocity(self,action):
        vx = self.actionDict.get(action).get('VX')
        vy = self.actionDict.get(action).get('VY')
        return vx,vy    
    
    def moveSnake(self):
        # function that moves the snake according to the action taken
        
        def convertToSnakeTile(id):
            # function that converts the tile to snake tile
            self.grid[id].isSnake = True
            self.grid[id].isNormal = False
            self.grid[id].defineTileColor()
        
        def convertToNormalTile(id):
            # function that converts the tile to snake tile
            self.grid[id].isSnake = False
            self.grid[id].isNormal = True
            self.grid[id].defineTileColor()
        
        vx,vy = self.getVelocity(self.currentAction)
        
        for i in range(len(self.snake)-1):
            
            if i==0:
                # converting the tail tile to normal tile
                convertToNormalTile(int(self.snake[0]))
            
            # the snake tail end shall follow the body before it.
            # in this way all the tiles except the head will follow the one before it.    
            self.snake[i]=self.snake[i+1]
            # converting the new moved tile to snake tile
            convertToSnakeTile(int(self.snake[i]))
        
        # moving the head according to the action taken
        self.snake[-1]+=vx+vy
        convertToSnakeTile(int(self.snake[-1]))
    
    def growSnake(self):
        """
        For all possible orientations of the tail the next tail to be added
        follows the same logic as given in the function
        """
        diff = self.snake[0] - self.snake[1]
        self.snake.insert(0,int(self.snake[0]+diff))
    
    def eatsApple(self):
        # function to see if the snake has eaten apple
        # if yes then the snake will grow by one unit
        if self.snake[-1] == self.appleId:
            self.grid[self.appleId].isApple = False 
            self.grid[self.appleId].defineTileColor()
            self.resetApple()
            self.growSnake()
            return True
        else:
            return False
    
    def goingBeyondWall(self,tileId,vx,vy):
        """FInds out if the velocity will make the pointer
        to go beyond the game border
        Args:
            tileId (int): the tile id before taking action
            vx (int): step in x direction
            vy (int): step in y direction
        """
        if not self.grid[tileId].isWall:
            return False
        else:
            if (tileId+vx+vy < 0) or (tileId+vx+vy>=self.gridSize*self.gridSize):
                return True
            elif (tileId%self.gridSize==self.gridSize-1) and ((tileId+vx+vy)%self.gridSize==0):
                # to see if the snake can step out of the grid going farther right
                return True
            elif ((tileId+vx+vy)%self.gridSize==self.gridSize-1) and ((tileId)%self.gridSize==0):
                # to see if the snake can step out of the grid going farther left
                return True
    
    def gameOver(self):
        # function to check if the player lost
        
        # see if the head of the snake is beyond the wall
        vx,vy = self.getVelocity(self.currentAction)
        beyondWall = self.goingBeyondWall(int(self.snake[-1]),vx,vy)
        snakeHead_nextStep = self.snake[-1]+vx+vy
        game_over = False
        if snakeHead_nextStep in self.snake:
            game_over = True
        
        return (game_over or beyondWall)