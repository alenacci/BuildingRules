import sys
#import and init pygame
import pygame
import building
pygame.init()

class Renderer:

    WHITE = [0,0,0]
    AZZURRO = [0,255,255]
    SIZE_X = 3
    SIZE_Y = 3


    def __init__(self):
        #create the screen
        window = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('Simulator')


    def drawTile(self, tile):
        if(tile.walkable == True):
            color = WHITE
        else:
            color = AZZURRO
        pygame.draw.rect(window, color, [tile.x, tile.y, SIZE_X, SIZE_Y])

    def drawBuilding(self):
        for row in building.grid.tiles:
            for tile in row:
                self.drawTile(tile)



