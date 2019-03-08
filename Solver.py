import numpy as np
import random

class MinesweeperSolver:
    def __init__(self, dim):
        self.cells = []
        self.dim = dim
        self.board = [[9 for i in range(self.dim)] for j in range(self.dim)]
        self.mines = []
        self.probability = np.array([[1 for i in range(self.dim)] for j in range(self.dim)], dtype = float)
        self.visited = []
        self.tmp = [[self.cells.append([i,j]) for i in range(self.dim)] for j in range(self.dim)]
        
    def getNeighborCells(self, cell):
        neighbors = []
        x, y = cell[0], cell[1]
        if x < self.dim-1:
            if y < self.dim-1:
                neighbors.append([x+1, y+1])
            if y > 0:
                neighbors.append([x+1, y-1])
            neighbors.append([x+1, y])
        if x > 0:
            if y < self.dim-1:
                neighbors.append([x-1, y+1])
            if y > 0:
                neighbors.append([x-1, y-1])
            neighbors.append([x-1, y])
        if y < self.dim-1:
            neighbors.append([x, y+1])
        if y > 0:
            neighbors.append([x, y-1])
        return neighbors
        
    def cellStatus(self, cell):
        clear = 0
        mine = 0
        unexplored = 0
        unexploredCells = []
        neighbors = self.getNeighborCells(cell)
        for a in neighbors:
            x, y = a[0], a[1]
            if self.board[x][y] >= 0 and self.board[x][y] != 9:
                clear += 1
            elif a in self.mines:
                mine += 1
            else:
                unexplored += 1
                unexploredCells.append(a)
        return [unexploredCells, unexplored, clear, mine]
    
    def updateProbability(self):
        for i in self.cells:
            x, y = i[0], i[1]
            ucells, u, c, m = self.cellStatus([x,y])
            if self.board[x][y] <= 0 or not ucells:
                self.probability[x][y] = 5
            elif self.board[x][y] != -1 and self.board[x][y] != 9:
                self.probability[x][y] = 5
                prob = (self.board[x][y] - m) / float(u)
                for k in ucells:
                    kx, ky = k[0], k[1]
                    if self.probability[kx][ky] != 1:
                        if self.probability[kx][ky] < prob:
                            self.probability[kx][ky] = prob
                    else:
                        self.probability[kx][ky] = prob
                
    def queryCell(self):
        min_x, min_y = np.where(self.probability == np.min(self.probability))
        r = random.randint(0, len(min_x)-1)
        x, y = min_x[r], min_y[r]
        if self.probability[x][y] >= 0.25:
            next_x, next_y = np.where(self.probability == 1)
            if(len(next_x)) == 0:
                return [x,y]
            ran = random.randint(0, len(next_x)-1)
            return [next_x[ran], next_y[ran]]
        return [x,y]
    
    def addVisitedCell(self, cell):
        if cell not in self.visited:
            self.visited.append(cell)
    
    def visitedCell(self, x, y, cell_val):
        self.board[x][y] = cell_val
        self.updateProbability()
        self.addVisitedCell([x,y])
        if cell_val == -1:
            self.addMineCell([x,y])
        elif [x,y] in self.mines:
            self.mines.remove([x,y])

    def addMineCell(self, cell):
        self.addVisitedCell(cell)
        if cell not in self.mines:
            self.board[cell[0]][cell[1]] = -1
            self.mines.append(cell)
            
    def unknownCell(self, cell):
        if self.board[cell[0]][cell[1]] not in [9,-1]:
            return False
        else:
            return True

    # Make deductions based on information retrieved from newly visited cell
    # Returns list of cells that are safe to visit and flags cells that must
    # be mines
    def queryDeductions(self):
        cellsToVisit = []

        # Explore all cells available
        for cell in self.cells:
            x, y = cell[0], cell[1]
            num_neighbors = len(self.getNeighborCells([x,y]))
            # Check if current cell is not a mine or unexplored
            if self.board[x][y] != -1 and self.board[x][y] != 9:
                val = self.board[x][y]               
                
                # If cell value is 0, then neighbors must be safe to visit
                if val == 0:
                    for cell in self.getNeighborCells([x,y]):
                        if self.unknownCell(cell):
                            cellsToVisit.append(cell)

                # if cell value is same as the number of flagged mines, then we must have already explored all mines                            
                ucells, num_unexplored, num_clear, num_explored_mines = self.cellStatus([x,y])
                if val == num_explored_mines:
                    for cell in ucells:
                        cellsToVisit.append(cell)
                        for neighbor in self.getNeighborCells(cell):
                            if self.unknownCell(neighbor):
                                cellsToVisit.append(neighbor)

                # if the number of unexplored cells is equal to value, they must all be mines, so flag them                                
                if val == (num_neighbors-num_clear):
                    for cell in ucells:
                        self.addMineCell(cell)
                        self.updateProbability()
        return cellsToVisit
            
    # Make further logical inferences based on new information
    def makeInferences(self):
        safeToVisit  = []
        inferred = 0

        # Nested for loop to enable comparison of each visited cell with the others
        for i in self.visited:
            for j in self.visited:
                if i != j:  
                    cell1, cell2 = i, j
                    x1, y1 = cell1[0], cell1[1]
                    x2, y2 = cell2[0], cell2[1]
                    ucells1, u1, c1, m1 = self.cellStatus(cell1)
                    ucells2, u2, c2, m2 = self.cellStatus(cell2)
                    
                    # Make tuples of unexplored neighbors for both cells
                    s1 = [tuple(i) for i in ucells1]
                    s2 = [tuple(j) for j in ucells2]
                    
                    # fetch the intersection of the tuples
                    common = set(s1).intersection(s2)

                    # if there are common neighbors, we can start to make inferences using what we know
                    if len(common) != 0:
                        # common UNEXPLORED neighbors is all neighbrors in set 1
                        if len(s1) < len(s2) and len(set(s1) - set(s2)) == 0:
                            diff = set(s2) - common
                            # Compute how many unexplored mines in both and take the difference
                            common_mines = abs(self.board[x1][y1] - m1 - self.board[x2][y2] + m2)
                            # If difference is zero, then all mines have been explored and the common
                            # neighbors are safe to explore
                            if common_mines == 0:
                                inferred = 1
                                for i in list(diff):
                                    safeToVisit.append(i)
                            # If difference isn't zero, but the list of common unkown mines is equal
                            # to the neighbors not shared, then those are the mines
                            else:
                                if len(diff) == common_mines:
                                    inferred = 1
                                    for i in list(diff):
                                        self.addMineCell([i[0],i[1]])
                        
                        # common neighbors is all neighbors in set 2
                        if len(s2) < len(s1) and len(set(s2) - set(s1)) == 0:
                            diff = set(s1) - common
                            # Compute how many unexplored mines in both and take the difference
                            common_mines = abs(self.board[x1][y1] - m1 - self.board[x2][y2] + m2)
                            # If difference is zero, then all mines have been explored and the common
                            # neighbors are safe to explore
                            if common_mines == 0:
                                inferred = 1
                                for i in list(diff):
                                    safeToVisit.append(i)
                            # If difference isn't zero, but the list of common unkown mines is equal
                            # to the neighbors not shared, then those are the mines
                            else:
                                if len(diff) == common_mines:
                                    inferred = 1
                                    for i in list(diff):
                                        self.addMineCell([i[0],i[1]])

                        # unexplored cells is the same length
                        if len(s1) == len(s2):
                            diff1 = set(s1) - common
                            diff2 = set(s2) - common

                            if len(diff1) == 1 and len(diff2) == 1:
                                ce1 = list(diff1)[0]
                                ce2 = list(diff2)[0]
                                v1 = self.board[ce1[0]][ce1[1]]
                                v2 = self.board[ce2[0]][ce2[1]]
                                if abs(v1-v2) == 1:
                                    inferred = 1
                                    if v1 < v2: 
                                        self.addMineCell(ce2)
                                        safeToVisit.append(ce1)
                                    else:
                                        self.addMineCell(ce1)
                                        safeToVisit.append(ce2)
        return safeToVisit   