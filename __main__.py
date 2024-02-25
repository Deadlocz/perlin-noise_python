from rich.console import Console
import math_helper as m
import random

""" default values """
# x, y are "chunk coordinates"
x = 0
y = 0
# res is the resolution the chunk is getting generated in
res = 16
# amount of chunks in width and height
chunksW = 3
chunksH = 3

# console for color printing with rich.console
console = Console()


class vect2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
def get_Color(value = 0):
    """ gets the correct color value, for a heightmap, with the given value """
    
    R = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, -0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1]
    """
    -1 -> 1 in 20 steps
    """
    # I know I probably shouldn't use a if else here but I'm to lazy to change that
    if R[1]    <= value <= R[0]:
        return "[red1]"
    elif R[2]  <= value <= R[1]:
        return "[orange_red1]"
    elif R[3]  <= value <= R[2]:
        return "[dark_orange]"
    elif R[4]  <= value <= R[3]:
        return "[orange1]"
    elif R[5]  <= value <= R[4]:
        return "[gold1]"
    elif R[6]  <= value <= R[5]:
        return "[yellow1]"
    elif R[7]  <= value <= R[6]:
        return "[yellow2]"
    elif R[8]  <= value <= R[7]:
        return "[green_yellow]"
    elif R[9]  <= value <= R[8]:
        return "[light_green]"
    elif R[10] <= value <= R[9]:
        return "[aquamarine1]"
    elif R[11] <= value <= R[10]:
        return "[dark_slate_gray1]"
    elif R[12] <= value <= R[11]:
        return "[sky_blue1]"
    elif R[13] <= value <= R[12]:
        return "[sky_blue3]"
    elif R[14] <= value <= R[13]:
        return "[cornflower_blue]"
    elif R[15] <= value <= R[14]:
        return "[slate_blue3]"
    elif R[16] <= value <= R[15]:
        return "[purple3]"
    elif R[17] <= value <= R[16]:
        return "[purple4]"
    elif R[18] <= value <= R[17]:
        return "[dark_magenta]"
    elif R[19] <= value <= R[18]:
        return "[dark_violet]"
    else:
        return "[black]"

def chunkDisplay(listData, resolution, width):
    """ generates a color 'heightmap' with the given data string """
    chunk = ""
    for index, data in enumerate(listData):
        color = get_Color(data)
        
        string = f"{color}# {color[0] + '/' + color[1::]}"
        chunk += string
        
        if (index+1) % (resolution*width) == 0:
            chunk += "\n"
    
    return chunk    
    
def getPermutationT(s=None):
    """ generates a randomized permutation table for perlin noise """
    P = []
    [P.append(i) for i in range(256)]
    
    for i in range(len(P)-1,0,-1):
        index = round(random.random()*(i-1))
        temp = P[i]
        
        P[i] = P[index]
        P[index] = temp
    
    P += P
    return P

seed = random.seed(input("Seed (can be left empty): "))
P = getPermutationT(seed)

def perlin(x, y): 
    """ generates perlin noise """
       
    def get_constant_vect(v):
        h = v % 3
        if h == 0:
            return vect2( 1.0, 1.0)
        elif h == 1:
            return vect2(-1.0, 1.0)
        elif h == 2:
            return vect2(-1.0,-1.0)
        else:
            return vect2( 1.0,-1.0)

    X = int(x) % 255
    Y = int(y) % 255
    
    xf = x - int(x)
    yf = y - int(y)
    
    topRight = vect2(xf-1.0, yf-1.0) 
    topLeft  = vect2(xf,     yf-1.0)
    botRight = vect2(xf-1.0, yf)
    botLeft  = vect2(xf,     yf)
    
    vTopRight = P[P[X+1]+Y+1]
    vTopLeft  = P[P[X  ]+Y+1]
    vBotRight = P[P[X+1]+Y  ]
    vBotLeft  = P[P[X  ]+Y  ]
    
    dTopRight = topRight.dot(get_constant_vect(vTopRight))
    dTopLeft  = topLeft.dot (get_constant_vect(vTopLeft ))
    dBotRight = botRight.dot(get_constant_vect(vBotRight))
    dBotLeft  = botLeft.dot (get_constant_vect(vBotLeft ))
    
    u = m.fade(xf)
    v = m.fade(yf)
    
    brightness = m.lerp2(u, m.lerp2(v, dBotLeft, dTopLeft), m.lerp2(v, dBotRight, dTopRight))
    return brightness\

def generateMap(x, y):
    """ generates a heighmap with given brightness data - here perlin noise """
    data = []
    chunks = []
    
    xB = x
    
    for i in range(res*chunksH):
        for j in range(res*chunksW):
            data.append(perlin(x, y))
            x += 1/res
        
        y += 1/res
        x = xB
    
    chunks.append(chunkDisplay(data, res, chunksW))
    console.print(chunks[0])
    
def movement(x, y):
    """ used for movement on the heigh map """
    s = " "
    mov = ["W", "A", "S", "D", "E", "e", "w", "a", "s", "d"]

    while s[0] not in mov:
        try:
            console.print(f"note: x/y values in the negative still bring some kind of error!")
            s = str(input(f"Cords: x={x}, y={y} | WASD: "))
        except ValueError as e:
            console.print(f"{e} | please only input one of the following letters: WASD")
        s += " "

    # yes, I like long if else statements :^)
    if s.startswith("w"):
        y += 1/res
    elif s.startswith("W"):
        y += 1
    elif s.startswith("d"):
        x += 1/res
    elif s.startswith("D"):
        x += 1
    elif s.startswith("s"):
        y -= 1/res
    elif s.startswith("S"):
        y -= 1
    elif s.startswith("a"):
        x -= 1/res
    elif s.startswith("A"):
        x -= 1
    elif s == "e" or s == "E":
        console.print(f"Seed: {seed}")
        exit()

    generateMap(x, y)
    return x, y

"""
! Minor Bugs:
! - terrain becomes repetitive with too big of a "view"
!  - easily visible at: (dunno if this is with EVERY seed tho)
!    x = 0, y = 0
!    res = 16
!    chunksW = 6, chunksH = 5
! - negative x and y values cause generation to basically 'die' lol
"""

generateMap(x, y)
while True:
    x, y = movement(x, y)
