FPS = 30

DIM=10
MINES=10

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