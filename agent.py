import numpy as np
from snakeEnv import snakeEnv, gridTile

class agent(snakeEnv):
    
    def __init__(self,gridSize):
        snakeEnv.__init__(self,gridSize)
        
        self.appleReward = 5
        self.snakeReward = -10
        self.beyondWallReward = -10
        self.tileReward = -1
        self.gamma = 0.9
        """
        Q table shall be a 2d matrix where number of rows 
        corresponds to the number of tiles in the grid and
        number of columns corresponds to the best action possible
        in that state and at the time step. Best action here 
        shall be the index value of possibleActions list
        """
        self.q = np.zeros((gridSize*gridSize,2))        
    
    def reward(self,tileId,isBeyondWall):
        """function that returns the reward for the requested tile ID

        Args:
            tileId (int): id of the tile
        """
        if isBeyondWall:
            reward = self.beyondWallReward
        else:
            reward = self.appleReward*self.grid[tileId].isApple + self.snakeReward*self.grid[tileId].isSnake + self.tileReward*self.grid[tileId].isNormal 
        
        return reward
    
    def learnQtable(self):
        # function that updates the q table before every move
        threshold = 0.01
        error = 1
        while error > threshold:
            # looping through all the tiles
            errorList = []
            for i in range(self.gridSize*self.gridSize):
                v = self.q[i,0]
                currentTileId = i
                possibleRewards = []
                # looping through possible actions
                for action in self.possibleActions:
                    vx,vy = self.getVelocity(action)
                    nextTileId = currentTileId+vx+vy
                    isBeyondWall = self.goingBeyondWall(currentTileId,vx,vy)
                    reward = self.reward(nextTileId,isBeyondWall)
                    if not isBeyondWall:
                        reward+= self.gamma*self.q[nextTileId,0]
                    possibleRewards.append(reward)
                maxIndx = np.argmax(possibleRewards)
                self.q[i,0] = possibleRewards[int(maxIndx)]
                self.q[i,1] = int(maxIndx)
                errorList.append(abs(v-self.q[i,0]))
            error = max(errorList)
    
    def takeAction(self):
        headId = int(self.snake[-1]) # current position of the head
        self.currentAction = self.possibleActions[int(self.q[headId,1])] # action that gives max reward

    def algorithm(self):
        """This is the main learning/playing part of the agent
        
        Returns:
            Boolean: level status whether the level is won or lost
        """
        self.learnQtable()
        print("Learnt the grid")
        self.takeAction()
        game_Over = self.gameOver() # checking if the action will lead to end of game
        if game_Over:
            self.gameReset()
            return False
        else:
            self.moveSnake()
            gameLevelUp = self.eatsApple()
            return game_Over,gameLevelUp

# snakeAgent = agent(20)