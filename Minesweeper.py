import numpy as np
import random, pygame, sys
from pygame.locals import *
import Constants
import Solver

def main():
    if Constants.USE_PREDEFINED_BOARD:
        board = Constants.BOARD
    else:
        board = generate_field(Constants.DIM, Constants.MINES)
        board = place_numbers(board, Constants.DIM)

    # initialize global variables & pygame module, set caption
    global FPSCLOCK, DISPLAYSURFACE, BASICFONT, RESET_SURF, RESET_RECT, SHOW_SURF, SHOW_RECT
    pygame.init()
    pygame.display.set_caption('Minesweeper')
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURFACE = pygame.display.set_mode((Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont(Constants.FONTTYPE, Constants.FONTSIZE)

    # Set background color
    DISPLAYSURFACE.fill(Constants.BGCOLOR)

    # Initialize Minesweeper Solver
    solver = Solver.MinesweeperSolver(Constants.DIM)

    while True:
        check_for_escape()

        # draw field
        DISPLAYSURFACE.fill(Constants.BGCOLOR)
        pygame.draw.rect(DISPLAYSURFACE, Constants.FIELDCOLOR, (Constants.XMARGIN-5, Constants.YMARGIN-5, (Constants.BOXSIZE+Constants.GAPSIZE)*Constants.DIM+5, (Constants.BOXSIZE+Constants.GAPSIZE)*Constants.DIM+5))
        draw_field(Constants.DIM)
        draw_values(board, Constants.DIM)

        play_next_move = False
        inferences_possible = False

        # event handling loop
        for event in pygame.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                terminate()
            elif event.type == MOUSEBUTTONDOWN:
                play_next_move = True

        if play_next_move and not checkGameStatus(board, solver):
            if not inferences_possible:
                # Start Solving for random cell by updating probability table and picking a random cell
                solver.updateProbability()
                coords = solver.queryCell()
                row, col = coords[0], coords[1]
                solver.visitedCell(row, col, board[row][col])
            
            # Make inferences and deductions from the knowledge obtained by querying the previous cell
            visitedCount = len(solver.visited)
            cellsToVisit = solver.queryDeductions()
            
            # Visit all cells that are deduced to be safe
            for cell in cellsToVisit:
                row, col = cell[0], cell[1]
                solver.visitedCell(row, col, board[row][col])
            
            cellsToVisit = solver.makeInferences()
            
            # Visit all cells that are inferred to be safe
            for cell in cellsToVisit:
                row, col = cell[0], cell[1]
                solver.visitedCell(row, col, board[row][col])

            # If deductions and inferences resulted in discovering more cells, rerun them while you keep
            # discovering more.
            if len(solver.visited) > visitedCount:
                inferences_possible = True
            else:
                inferences_possible = False

        # redraw cover, screen, and wait clock tick
        draw_covers(solver.visited, solver.mines)
        pygame.display.update()
        FPSCLOCK.tick(Constants.FPS)

def draw_field(dim):
    for row in range(dim):
        for col in range(dim):
            top, left = topleft_coords(row, col)
            pygame.draw.rect(DISPLAYSURFACE, Constants.BOXCOLOR_REV, (left, top, Constants.BOXSIZE, Constants.BOXSIZE))

def draw_values(field,dim):
    half = int(Constants.BOXSIZE*0.5)
    quarter = int(Constants.BOXSIZE*0.25)
    eighth = int(Constants.BOXSIZE*0.125)

    for row in range(dim):
        for col in range(dim):
            top, left = topleft_coords(row, col)
            center_x, center_y = center_coords(row, col)
            if mine_exists(field, row, col):
                pygame.draw.circle(DISPLAYSURFACE, Constants.MINECOLOR, (left+half, top+half), quarter)
                pygame.draw.circle(DISPLAYSURFACE, Constants.WHITE, (left+half, top+half), eighth)
                pygame.draw.line(DISPLAYSURFACE, Constants.MINECOLOR, (left+eighth, top+half), (left+half+quarter+eighth, top+half))
                pygame.draw.line(DISPLAYSURFACE, Constants.MINECOLOR, (left+half, top+eighth), (left+half, top+half+quarter+eighth))
                pygame.draw.line(DISPLAYSURFACE, Constants.MINECOLOR, (left+quarter, top+quarter), (left+half+quarter, top+half+quarter))
                pygame.draw.line(DISPLAYSURFACE, Constants.MINECOLOR, (left+quarter, top+half+quarter), (left+half+quarter, top+quarter))
            else:
                val = int(field[row][col])
                if val==0:
                    textColor = Constants.GREEN
                elif val in range(1,3):
                    textColor = Constants.BLUE
                else:
                    textColor = Constants.RED
                draw_text(str(val), BASICFONT, textColor, DISPLAYSURFACE, center_x, center_y)
                
def draw_covers(revealedBoxes, markedMines):
    for row in range(Constants.DIM):
        for col in range(Constants.DIM):
            if [row,col] not in revealedBoxes:
                top, left = topleft_coords(row, col)
                pygame.draw.rect(DISPLAYSURFACE, Constants.BOXCOLOR_COV, (left, top, Constants.BOXSIZE, Constants.BOXSIZE))
            else:
                if [row,col] in markedMines:
                    top, left = topleft_coords(row, col)
                    pygame.draw.rect(DISPLAYSURFACE, Constants.MINEMARK_COV, (left, top, Constants.BOXSIZE, Constants.BOXSIZE))

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

def topleft_coords(row, col):
    top = Constants.YMARGIN + row * (Constants.BOXSIZE + Constants.GAPSIZE)
    left = Constants.XMARGIN + col * (Constants.BOXSIZE + Constants.GAPSIZE)
    return top, left

def center_coords(row, col):
    center_x = Constants.XMARGIN + (Constants.BOXSIZE/2) + col*(Constants.BOXSIZE + Constants.GAPSIZE)
    center_y = Constants.YMARGIN + (Constants.BOXSIZE/2) + row*(Constants.BOXSIZE + Constants.GAPSIZE)
    return center_x, center_y

def checkGameStatus(board, solver):
    for i in solver.cells:
        x,y = i[0], i[1]
        if board[x][y] == -1 and [x,y] not in solver.mines:
            return False
    return True

def generate_field(dim, mines):
    field = np.zeros((dim,dim))
    for i in range(mines):
        field[i % dim][divmod(i,dim)[0]] = -1       
    for i in range(4):
        field = np.rot90(field)
        for row in range(dim):
            np.random.shuffle(field[row])
    return field

def mine_exists(field, row, col):
    return field[row][col] == -1

def place_numbers(field, dim):
    for row in range(dim):
        for col in range(dim):
            if not mine_exists(field,row,col):
                field[row][col]=count_mines(field, dim, row, col)
    return field

def count_mines(field, dim, row, col):
    count=0
    if row > 0 and col > 0:
        if mine_exists(field, row-1, col-1):
            count += 1
    if row > 0:
        if mine_exists(field, row-1, col):
            count += 1
    if row > 0 and col < (dim-1):
        if mine_exists(field, row-1, col+1):
            count += 1
    if col < (dim-1):
        if mine_exists(field, row, col+1):
            count += 1
    if row < (dim-1) and col < (dim-1):
        if mine_exists(field, row+1, col+1):
            count += 1
    if row < (dim-1):
        if mine_exists(field, row+1, col):
            count += 1
    if row < (dim-1) and col > 0:
        if mine_exists(field, row+1, col-1):
            count += 1
    if col > 0:
        if mine_exists(field, row, col-1):
            count += 1
    return count

def terminate():
    pygame.quit()
    sys.exit()

def check_for_escape():
    events = pygame.event.get(KEYUP)
    if len(events) == 0:
        return None
    if events[0].key == K_ESCAPE:
        terminate()
    return events[0].key

if __name__ == '__main__':
    main()