import noise
from rich.console import Console
import time

""" default values """
# x, y are "chunk coordinates"
x = 0
y = 0
# res is the resolution the chunk is getting generated in
res = 16
# amount of chunks in width and height
chunksW = 5
chunksH = 3

# console for color printing with rich.console
console = Console()
P, seed = noise.getPermutationT()

def get_Color(value = 0, previous= 0):
    """ gets the correct color value, for a heightmap, with the given value """

    heightV = {1 : "red1", 0.9 : "orange_red1", 0.8 : "dark_orange", 0.7 : "orange1", 0.6: "gold1",
         0.5: "yellow1", 0.4 : "yellow2", 0.3 : "green_yellow", 0.2 : "light_green", 0.1 : "aquamarine1",
         0: "dark_slate_gray1", -0.1 : "sky_blue1", -0.2 : "sky_blue3", -0.3 : "cornflower_blue", -0.4 : "slate_blue3",
         -0.5 : "purple3", -0.6 : "purple4", -0.7 : "dark_magenta", -0.8 : "dark_violet", -0.9 : "dark_magenta", -1 : "dark_magenta"}

    if value >= -1 and value <= 1:
        return heightV[round(value,1)]
    elif previous >= -1 and previous <= 1:
        return heightV[round(previous, 1)]
    elif value > 1:
        return heightV[1]
    else:
        return heightV[-1]
    
def chunkDisplay(listData, resolution, width):
    """ generates a color 'heightmap' with the given data string """

    chunk = ""
    color = ""
    previousValue = 0
    for index, data in enumerate(listData):
        
        color = get_Color(data, previousValue)
        if not(previousValue > 1 or previousValue < -1):
            previousValue = data
        
        string = f"{'[' + color + ']'}##{'[/' + color + ']'}"
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
            n = amplitude * noise.perlin((x if x > -0.1 else x*-1) * frequency, (y if y > -0.1 else y*-1) * frequency, P)
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
            pixel = round(FractalBrownianMotion(x, y, 8), 5)
            data.append(pixel)
            x += 1/res
                
        y += 1/res
        x = xB

    chunks.insert(0,(chunkDisplay(data, res, chunksW)))
    console.print(chunks[0])
     
def movement(x, y):
    """ used for movement on the heigh map """
    s = " "
    mov = ["W", "A", "S", "D", "E", "e", "w", "a", "s", "d"]

    while s[0] not in mov:
        try:
            console.print(f"note: x/y values in the negative will 'copy' the brightness of their positive values!")
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

generateMap(x, y)
while True:
    x, y = movement(x, y)
