import cv2
import os
import numpy as np
import random

tile_size = 60
grid_size = 8

os.system('cls' if os.name == 'nt' else 'clear')
print("\n\n\n\n")

class Cell:
    def __init__(self, tiles, collapsed, entrophy, position, changed):
        self.tiles = tiles
        self.collapsed = collapsed
        self.entrophy = entrophy
        self.position = position
        self.changed = changed
        

class Tile: 
     def __init__(self, tileimage, tileconnections):
         self.tileimage = tileimage
         self.tileconnections = tileconnections
         self.id = 0

folder = 'wfc/maditiles'

tileimages = []
for filename in os.listdir(folder):
    img = cv2.imread(os.path.join(folder, filename))
    newimg = cv2.resize(img,[tile_size,tile_size],interpolation = cv2.INTER_AREA)
    tileimages.append(newimg)

tiles = []
tiles.append(Tile(tileimages[0], (0,0,0,0)))
tiles.append(Tile(tileimages[1], (1,0,1,0)))
tiles.append(Tile(tileimages[2], (0,1,0,1)))
tiles.append(Tile(tileimages[3], (0,1,1,0)))
tiles.append(Tile(tileimages[4], (0,0,1,1)))
tiles.append(Tile(tileimages[5], (1,0,0,1)))
tiles.append(Tile(tileimages[6], (1,1,0,0)))
tiles.append(Tile(tileimages[7], (1,1,1,1)))
tiles.append(Tile(tileimages[8], (1,1,1,1)))
tiles.append(Tile(tileimages[9], (1,0,1,1)))
tiles.append(Tile(tileimages[10], (1,1,0,1)))
tiles.append(Tile(tileimages[11], (1,1,1,0)))
tiles.append(Tile(tileimages[12], (0,1,1,1)))
tiles.append(Tile(tileimages[13], (1,1,1,1)))
tiles.append(Tile(tileimages[14], (1,1,1,1)))
tiles.append(Tile(tileimages[15], (1,1,1,1)))
tiles.append(Tile(tileimages[16], (1,1,1,1)))
tiles.append(Tile(tileimages[17], (1,1,1,0)))
tiles.append(Tile(tileimages[18], (0,1,1,1)))
tiles.append(Tile(tileimages[19], (1,0,1,1)))
tiles.append(Tile(tileimages[20], (1,1,0,1)))
tiles.append(Tile(tileimages[21], (1,0,1,1)))
tiles.append(Tile(tileimages[22], (1,1,0,1)))
tiles.append(Tile(tileimages[23], (1,1,1,0)))
tiles.append(Tile(tileimages[24], (0,1,1,1)))
tiles.append(Tile(tileimages[25], (1,1,1,1)))
tiles.append(Tile(tileimages[26], (1,1,1,1)))
tiles.append(Tile(tileimages[27], (1,1,1,1)))
tiles.append(Tile(tileimages[28], (1,1,1,1)))
tiles.append(Tile(tileimages[29], (1,1,1,1)))
tiles.append(Tile(tileimages[30], (1,1,1,1)))
tiles.append(Tile(tileimages[31], (1,1,1,1)))
tiles.append(Tile(tileimages[32], (1,1,1,1)))

for index, tile in enumerate(tiles):
    tile.id = index 

tileamount = len(tileimages)
output_size = tile_size * tileamount

image = np.zeros((output_size, tile_size, 3), dtype=np.uint8)

filenames = os.listdir(folder)
filenames.sort(key=lambda x: int(x.split(".")[0]))

output_width = grid_size * tile_size
output_height = grid_size * tile_size

output_image = np.zeros((output_height, output_width, 3), dtype=np.uint8)

grid = np.empty((grid_size, grid_size), dtype=object)

#assign fresh cells to the grid
for i in range(grid_size):
    for j in range(grid_size):
        grid[i][j] = Cell(tiles, 0, len(tiles), (i, j), 1)

print("\n\n\n.... STARTING")

def checkPos(cPos, checkDir):
    return (cPos[0] + checkDir[0], cPos[1] + checkDir[1])

iteration = 1

import time
start_time = time.time()

while True:

    try:
        print("\nITERATION:", iteration)

        if(iteration == 1):
            previousGrid = grid

        workingGrid = grid

        for x in range(grid_size):
            for y in range(grid_size):
                if(len(grid[x][y].tiles) != len(previousGrid[x][y].tiles)):
                    grid[x][y].changed = 1
                else:
                    grid[x][y].changed = 0

        previousGrid = grid

        for x in range(grid_size):
            for y in range(grid_size):

                currentCell = workingGrid[x][y]

                if(currentCell.collapsed != 1 and currentCell.changed == 0):

                    currentCellTiles = currentCell.tiles

                    currentPos = (x, y)
                    upCheck = checkPos(currentPos, (-1, 0))
                    rightCheck = checkPos(currentPos, (0, 1))
                    downCheck = checkPos(currentPos, (1, 0))
                    leftCheck = checkPos(currentPos, (0, -1))

                    currentCellConnections = []
                    connectionIndex = []

                    for index, cellTile in enumerate(currentCellTiles):

                        currentConnection = cellTile.tileconnections

                        vote = 0
                        #UP CHECK            
                        if(upCheck[0] >= 0):       
                            checkCell = workingGrid[x - 1][y]
                            currentCheckCellTiles = checkCell.tiles 
                            for tile in currentCheckCellTiles:
                                if(currentConnection[0] == tile.tileconnections[2]):
                                    vote += 1
                                    break
                        else:
                            vote += 1

                        #RIGHT CHECK             
                        if(rightCheck[1] <= grid_size - 1):
                            checkCell = workingGrid[x][y + 1]                       
                            currentCheckCellTiles = checkCell.tiles
                            for tile in currentCheckCellTiles:
                                if(currentConnection[1] == tile.tileconnections[3]):
                                    vote += 1
                                    break
                        else:
                            vote += 1


                        #DOWN CHECK
                        if(downCheck[0] <= grid_size - 1):
                            checkCell = workingGrid[x + 1][y]                     
                            currentCheckCellTiles = checkCell.tiles
                            for tile in currentCheckCellTiles:
                                if(currentConnection[2] == tile.tileconnections[0]):
                                    vote += 1
                                    break
                        else:
                            vote += 1

                        #LEFT CHECK
                        if(leftCheck[1] >= 0):
                            checkCell = workingGrid[x][y - 1]
                            currentCheckCellTiles = checkCell.tiles
                            for tile in currentCheckCellTiles:
                                if(currentConnection[3] == tile.tileconnections[1]):
                                    vote += 1
                                    break
                        else:
                            vote += 1

                        if(vote == 4):
                            connectionIndex.append(cellTile)

                    grid[x][y].changed = 0

                    grid[x][y].tiles = connectionIndex
                    grid[x][y].entrophy = len(connectionIndex) - 1

        entrophyList = np.zeros((grid_size, grid_size))

        for x in range(grid_size):
            for y in range(grid_size):
                entrophyList[x][y] = grid[x][y].entrophy

        listOfCordinates = []
        smallestEntrophyList = []

        result = np.min(entrophyList[entrophyList>0])

        for x in range(grid_size):
            for y in range(grid_size):
                currentIndex = entrophyList[x][y]
                if(int(currentIndex) == int(result)):
                    listOfCordinates.append((x, y))

        randomCoord = random.choice(listOfCordinates)

        randomInt = random.randint(0, len(listOfCordinates))
        collapseCoords = random.choice(listOfCordinates)

        cx, cy = collapseCoords[0], collapseCoords[1]

        currentTileList = grid[cx][cy].tiles

        randomTile = random.choice(currentTileList)

        templist = []
        for temp in currentTileList:
            templist.append(temp.id)

        randomTileList = []
        randomTileList.append(randomTile)

        grid[cx][cy].tiles = randomTileList
        grid[cx][cy].collapsed = 1
        grid[cx][cy].entrophy = -1
        grid[cx][cy].changed = 1

        iteration += 1

        if(iteration == grid_size * grid_size + 1):
            break

    except ValueError:
        for i in range(grid_size):
            for j in range(grid_size):
                grid[i][j] = Cell(tiles, 0, len(tiles), (i, j), 0)
                print("\nRESTARTING\n")
                iteration = 1
        start_time = time.time()

print("\n.... DONE")
print(".... PROCESSING TIME: %s seconds" % (time.time() - start_time))

itergrid = grid.flatten()
for i, filename in enumerate(itergrid):
    if(len(filename.tiles) > 0):
        filename.tiles = [filename.tiles[0]]

    currenttileimage = filename.tiles

    x = (i % grid_size) * tile_size
    y = (i // grid_size) * tile_size

    output_image[y:y+tile_size, x:x+tile_size] = currenttileimage[0].tileimage

cv2.imshow('Canvas', output_image)
cv2.imwrite('wfc/image.png', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
