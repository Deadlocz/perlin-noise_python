import random
import math_helper as m

class vect2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    

def getPermutationT():
    """ generates a randomized permutation table for perlin noise """
    
    s = input("Seed (can be left empty): ")
    if s == "":
        s = (random.randint(random.randint(0,65536),random.randint(65537,131072)))
        random.seed(s)
    else:
        random.seed(s)
        
    P = []
    [P.append(i) for i in range(256)]
    
    for i in range(len(P)-1,0,-1):
        index = round(random.random()*(i-1))
        temp = P[i]
        
        P[i] = P[index]
        P[index] = temp
    
    P += P
    return P,s


def perlin(x, y, P): 
    """ generates perlin noise for a single pixel using a given Permutation table `P` """
    #! kinda fixes the negative number issue? not really                                                     
    """         
    if x < 0: 
        x *= -1
    if y < 0:
        y *= -1
    """
       
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

    X = int(x) & 255
    Y = int(y) & 255
    
    
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
    
    return m.lerp2(u, m.lerp2(v, dBotLeft, dTopLeft), m.lerp2(v, dBotRight, dTopRight))

