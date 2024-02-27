import noise
from rich.console import Console


""" default values """
# x, y are "chunk coordinates"
x = 0
y = 0
# res is the resolution the chunk is getting generated in
res = 16
# amount of chunks in width and height
chunksW = 7
chunksH = 3

# console for color printing with rich.console
console = Console()
P, seed = noise.getPermutationT()

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
    

def generateMap(x, y):
    """ generates a heighmap with given brightness data - here perlin noise """
    
    def FractalBrownianMotion(x, y, numOctaves):
        """ Fractal Brownian Motion to create a more natural feel to the heightmap """
        result = 0
        amplitude = 1.0
        frequency = 0.5
        
        for o in range(numOctaves):
            n = amplitude * noise.perlin(x * frequency, y * frequency, P)
            result += n

            amplitude *= 0.5
            frequency *= 2.0
        
        return result
            
    data = []
    chunks = []
    
    xB = x
    

    # freq res
    for i in range(res*chunksH):
        for j in range(res*chunksW):
            data.append(FractalBrownianMotion(x, y, 8))
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
    elif s.startswith("e") or s.startswith("E"):
        console.print(f"Seed: {seed}")
        input("You can now close this window with Enter.") 
        exit()

    generateMap(x, y)
    return x, y

"""
! Minor Bugs:
! - sometimes generates values out of range of the colors
"""

generateMap(x, y)
while True:
    x, y = movement(x, y)
