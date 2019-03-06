import numpy as np
import random

minesweeperboard = [[3, -1, 3, 2, 2],
 [-1, -1, 3, -1, -1],
 [3, 3, 3, 2, 2],
 [2, -1, 2, 0, 0],
 [2, -1, 2, 0, 0]]

class minesweeperSolver:
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
    
    def checkCell(self, cell):
        x, y = cell[0], cell[1]
        print('Checking Cell[',x,'][',y,']')
        self.board[x][y] = minesweeperboard[x][y]
        self.updateProbability()
        if self.board[x][y] == -1:
            print('Ran into a mine')
            self.addMineCell(cell)
    
    def addMineCell(self, cell):
        if cell not in self.mines:
            self.board[cell[0]][cell[1]] = -1
            self.mines.append(cell)
            
    def addVisitedCells(self):
        self.visited = []
        for i in self.cells:
            if not self.unknownCell(i):
                if self.cellStatus(i)[1]:
                    self.visited.append(i)
                    
    def exploreCell(self, cell):
        for x in self.getNeighborCells(cell):
            self.searchCells(cell)
            
    def unknownCell(self, cell):
        if self.board[cell[0]][cell[1]] not in [9,-1]:
            return False
        else:
            return True
            
    def searchCells(self, cell):
        j, k = cell[0], cell[1]
        if j == 500 or k == 500:
            search = self.cells
        else:
            search = [cell]
        
        for i in search:
            x, y = i[0], i[1]
            n = len(self.getNeighborCells([x,y]))
            if self.board[x][y] != -1 and self.board[x][y] != 9:
                v = self.board[x][y]               
                if v == 0:
                    for a in self.getNeighborCells([x,y]):
                        if self.unknownCell(a):
                            self.checkCell(a)
                ucells, u, c, m = self.cellStatus([x,y])
                print('Cell:',x,',',y)
                print('Ucells:',ucells,'u:',u,'c:',c,'m:',m,'v:',v,'n:',n)
                if v == m:
                    for b in ucells:
                        self.checkCell(b)
                        print('u1')
                        for u in self.getNeighborCells(b):
                            if self.unknownCell(u):
                                print('u2')
                                self.searchCells(u)
                if v == (n-c):
                    for c in ucells:
                        self.addMineCell(c)
                        self.updateProbability()
                    
    def inferClues(self):
        inferred = 0
        for i in self.visited:
            for j in self.visited:
                if i != j:
                    cell1, cell2 = i, j
                    x1, y1 = cell1[0], cell1[1]
                    x2, y2 = cell2[0], cell2[1]
                    ucells1, u1, c1, m1 = self.cellStatus(cell1)
                    ucells2, u2, c2, m2 = self.cellStatus(cell2)
                    s1 = [tuple(i) for i in ucells1]
                    s2 = [tuple(j) for j in ucells2]
                    common = set(s1).intersection(s2)
                    if len(common) != 0:
                        if len(s1) < len(s2) and len(set(s1) - set(s2)) == 0:
                            diff = set(s2) - common
                            common_mines = abs(self.board[x1][y1] - m1 - self.board[x2][y2] + m2)
                            if common_mines == 0:
                                inferred = 1
                                for i in list(diff):
                                    self.checkCell([i[0],i[1]])
                            else:
                                if len(diff) == common_mines:
                                    inferred = 1
                                    for i in list(diff):
                                        self.addMineCell([i[0],i[1]])
                        if len(s2) < len(s1) and len(set(s2) - set(s1)) == 0:
                            diff = set(s1) - common
                            common_mines = abs(self.board[x1][y1] - m1 - self.board[x2][y2] + m2)
                            if common_mines == 0:
                                inferred = 1
                                for i in list(diff):
                                    self.checkCell([i[0],i[1]])
                            else:
                                if len(diff) == common_mines:
                                    inferred = 1
                                    for i in list(diff):
                                        self.addMineCell([i[0],i[1]])
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
                                        self.checkCell(ce1)
                                    else:
                                        self.addMineCell(ce1)
                                        self.checkCell(ce2)
        if inferred == 1:
            print("Found open cells using clues")
                                
    def checkGameStatus(self):
        for i in self.cells:
            x,y = i[0], i[1]
            if minesweeperboard[x][y] == -1 and [x,y] not in self.mines:
                return False
        return True   
    
    def cellsFound(self):
        c = 0
        for i in self.cells:
            if self.board[i[0]][i[1]] != 9:
                c += 1
        return c
        
        
    def solve(self):
        while not self.checkGameStatus():
            self.updateProbability()
            self.checkCell(self.queryCell())
            c = self.cellsFound()
            self.searchCells([500,500])
            self.addVisitedCells()
            self.inferClues()
            while(self.cellsFound() > c):
                c = self.cellsFound()
                self.searchCells([500,500])
                self.addVisitedCells()
                self.inferClues()
                
m = minesweeperSolver(5)

m.board

m.probability

m.solve()

m.board