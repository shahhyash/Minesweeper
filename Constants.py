FPS = 30

#  If using predefined board, make sure DIM and MINES reflect the right value
USE_PREDEFINED_BOARD=False
BOARD=[
    [ 1, -1,  3, -1,  2],
    [ 1,  1,  4, -1,  3],
    [ 1,  1,  2, -1,  2],
    [-1,  1,  1,  1,  1],
    [ 1,  1,  0,  0,  0],
]

DIM=5
MINES=5

BOXSIZE = 30
GAPSIZE = 5

XMARGIN = 50
YMARGIN = XMARGIN

WINDOWWIDTH = DIM * (BOXSIZE+GAPSIZE) + (XMARGIN * 2)
WINDOWHEIGHT = DIM * (BOXSIZE+GAPSIZE) + (YMARGIN * 2)

# assign colors 
LIGHTGRAY = (225, 225, 225)
DARKGRAY = (160, 160, 160)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)

# set up major colors
BGCOLOR = WHITE
FIELDCOLOR = BLACK
BOXCOLOR_COV = DARKGRAY # covered box color
BOXCOLOR_REV = LIGHTGRAY # revealed box color
MINECOLOR = BLACK
TEXTCOLOR_1 = BLUE
TEXTCOLOR_2 = RED
TEXTCOLOR_3 = BLACK
HILITECOLOR = GREEN
RESETBGCOLOR = LIGHTGRAY
MINEMARK_COV = RED

# set up font 
FONTTYPE = 'Courier New'
FONTSIZE = 20