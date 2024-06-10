import pygame
import sys

from noise import perlin, getPermutationT

class Noise:
    def __init__(self, res=64):
            pygame.init()
            
            pygame.display.set_caption("Perlin Noise Tech Demo")
            
            self.res = res
            
            self.clock = pygame.time.Clock()
            
            self.screen = pygame.display.set_mode((1680, 945))
            self.screen_size = self.screen.get_size()
            self.display = pygame.Surface(((16 * self.res/3), (9 * self.res/3)))
            self.display_size = self.display.get_size()

            self.permutation, self.seed = getPermutationT()
            self.data = []
    
    def get_Color(self, value=0):
        """ gets the correct color value, for a heightmap, with the given value """
        heightV = {
            1 : (255, 0, 0),
            0.9 : (255, 102, 0),
            0.8 : (255, 153, 51),
            0.7 : (255, 204, 0),
            0.6: (255, 255, 0),
            0.5: (204, 255, 51),
            0.4 : (153, 255, 51),
            0.3 : (102, 255, 51), 
            0.2 : (0, 255, 0), 
            0.1 : (102, 255, 204),
            0: (0, 255, 255), 
            -0.1 : (0, 153, 255), 
            -0.2 : (0, 102, 255), 
            -0.3 : (102, 153, 255), 
            -0.4 : (153, 153, 255),
            -0.5 : (204, 102, 255), 
            -0.6 : (153, 51, 255), 
            -0.7 : (153, 0, 255), 
            -0.8 : (102, 0, 204), 
            -0.9 : (90, 0, 180), 
            -1 : (102, 102, 153)
        } 

        #print(value)
        if value >= -1 and value <= 1:
            return heightV[round(value,1)]
        elif value > 1:
            return (255, 0, 0)
        elif value < -1:
            return (102, 102, 153)
        else:
            print(value)
            return (0, 0, 0)

    
    def generateMap(self, x, y):
        
        def FractalBrownianMotion(x, y, numOctaves):
            result = 0 
            amplitude = 1.0
            frequency = 0.5
            
            for o in range(numOctaves):
                n = amplitude * perlin((x if x > -0.1 else x * -1) * frequency, (y if y > -0.1 else y * -1) * frequency, self.permutation)
                result += n

                amplitude *= 0.5
                frequency *= 2.0
                
            return result 
        xB = x
    
        for i in range(self.display_size[1]):
            for j in range(self.display_size[0]):
                pixel = round(FractalBrownianMotion(x, y, 4), 5)
                x += 1/self.res
                self.data.append([pixel, pygame.Rect(j, i, 1, 1)])
                
            y += 1/self.res
            x = xB

    def run(self):
        x = 0
        y = 0
        while True:
            self.display.fill((0, 0, 0))
            self.generateMap(x, y)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            for rect in self.data:
                color = self.get_Color(value=float(rect[0]))
                pygame.draw.rect(self.display, color, rect[1])
                
            
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(2)
            print("passed")
            x += 1
            
Noise().run()