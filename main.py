# Import libraries and define initial values
import pygame
import math
import time
import sys
import threading

# from random import seed
from random import randint  # Random numb. generator

# Configure initial values
global snakePathData, snakeDirection, score, gameOver, timer

clock = pygame.time.Clock()
timer = 0
timeTillNextTick = 0.8
bkgColor = 0, 0, 0
gameBoard = []
colors = {0: (255, 255, 255), 3: (153, 71, 253), 2: (39, 78, 19), 1: (6, 246, 45), 4: (255, 45, 3)}
snakePathData = []
snakeDirection = 0  # 0 = Up, 1 = Down, 2 = Right, 3 = Left
score = 0
gameOver = False

"""
BLOCK TYPES
0 = Air
1 = Head
2 = Body
3 = Wall
4 = Apple

BLOCK TYPES -> PARAMS
isHead - Defines if the block type is the head.
isBody - Defines if the block type is a movable part of the body.
isWall - Defines if the block will end the game if touched by a block with isHead.
consumable - Defines if a block will score a point.

SNAKE PATH DATA
This list contains dictionaries storing information about the path taken by the snake.
Every time the snake increases in length, the list deletes the last value, and creates
new values everytime the snake eats apples. Deleted values get supplemented by a new
positional value in the first slot of the list, refilling this index everytime the screen
updates to move the snake and register game events.
For example:
[[5, 5], [4, 5], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1]]
That would generate a snake body 7 body blocks long, and create a L-shape, starting from
(5, 5), with the corner at (3, 5), and ending at (3,1), followed by the head at (3, 0),
which would cause a game over since the y value is == 0.

"""


# Function calls

class Snake:
    def __init__(self):
        pass

    @staticmethod
    def spawnMatrix(w, h):
        print("[ i ] Generating " + str(w) + "x" + str(h) + " matrix...")
        for x in range(h):
            a = []
            for y in range(w):
                if x == 0 or x + 1 == h:
                    a.append(3)
                else:
                    if len(a) == 0 or len(a) + 1 == w:
                        a.append(3)
                    else:
                        a.append(0)
            gameBoard.append(a)
        print("[ i ] Done generating matrix.")

    @staticmethod
    def spawnRandApples(x):
        global gameBoard
        for y in range(x):
            randData = Snake.randNumbGen()
            gameBoard[randData["y"]][randData["x"]] = 4
            print("[ i ] Generated apple at (" + str(randData["x"]) + ", " + str(randData["y"]) + ").")

    @staticmethod
    def randNumbGen():
        x = randint(1, (len(gameBoard[0]) - 2))
        y = randint(1, (len(gameBoard) - 2))
        return dict(y=y, x=x)

    @staticmethod
    def draw():
        for y in range(len(gameBoard)):
            for x in range(len(gameBoard[y])):
                rect = ((x * 25), (y * 25), 25, 25)
                pygame.draw.rect(background, colors[gameBoard[y][x]], rect)

    @staticmethod
    def spawnSnake(size):
        global snakePathData
        snakePathData = []
        index = len(gameBoard) // 2
        index2 = len(gameBoard[index]) // 2
        gameBoard[index][index2] = 1
        snakePathData.append({"x": index2, "y": index})
        for x in range(size-1):
            gameBoard[(index + (x + 1))][index2] = 2
            snakePathData.append({"x": index2, "y": (index+(x+1))})

    @staticmethod
    def locateHead():
        rt = {"x": -1, "y": -1}
        for y in range(len(gameBoard)):
            for x in range(len(gameBoard[y])):
                if gameBoard[y][x] == 1:
                    rt["x"] = x
                    rt["y"] = y
                    return rt

    @staticmethod
    def locateBodyBlocks():
        rt = []
        for y in range(len(gameBoard)):
            for x in range(len(gameBoard[y])):
                if gameBoard[y][x] == 2:
                    rt.append({"x": x, "y": y})
        return rt

    @staticmethod
    def processBody():
        global snakeDirection, score, timeTillNextTick, gameOver, snakePathData
        headLocation = Snake.locateHead()
        # Replace current location with a body block
        gameBoard[headLocation["y"]][headLocation["x"]] = 2
        # Update body
        gameBoard[snakePathData[len(snakePathData) - 1]["y"]][snakePathData[len(snakePathData) - 1]["x"]] = 0
        snakePathData.pop(len(snakePathData) - 1)
        snakePathData = Snake.locateBodyBlocks()
        # Process input and modify data to represent changes
        if snakeDirection == 0:  # Snake is facing upwards
            # Check for objects
            if gameBoard[headLocation["y"] - 1][headLocation["x"]] == 3 or gameBoard[headLocation["y"] - 1][headLocation["x"]] == 2:  # Wall
                gameOver = True
                print("Game over!")
                return
            elif gameBoard[headLocation["y"] - 1][headLocation["x"]] == 4:  # Apple
                score += 100
                print("Yummy!")
                if not timeTillNextTick <= 0.1:
                    timeTillNextTick -= 0.025
            headLocation["y"] -= 1
            # Replace new head location with a head block
            gameBoard[headLocation["y"]][headLocation["x"]] = 1

        elif snakeDirection == 1:  # Snake is facing downwards
            # Check for objects
            if gameBoard[headLocation["y"] + 1][headLocation["x"]] == 3 or gameBoard[headLocation["y"] + 1][headLocation["x"]] == 2:  # Wall
                gameOver = True
                print("Game over!")
                return
            elif gameBoard[headLocation["y"] + 1][headLocation["x"]] == 4:  # Apple
                score += 100
                print("Yummy!")
                if not timeTillNextTick <= 0.1:
                    timeTillNextTick -= 0.025
            headLocation["y"] += 1
            # Replace new head location with a head block
            gameBoard[headLocation["y"]][headLocation["x"]] = 1

        elif snakeDirection == 2:  # Snake is facing right
            # Check for objects
            if gameBoard[headLocation["y"]][headLocation["x"] + 1] == 3 or gameBoard[headLocation["y"]][headLocation["x"] + 1] == 2:  # Wall
                gameOver = True
                print("Game over!")
                return
            elif gameBoard[headLocation["y"]][headLocation["x"] + 1] == 4:  # Apple
                score += 100
                print("Yummy!")
                if not timeTillNextTick <= 0.1:
                    timeTillNextTick -= 0.025
            headLocation["x"] += 1
            # Replace new head location with a head block
            gameBoard[headLocation["y"]][headLocation["x"]] = 1

        elif snakeDirection == 3:  # Snake is facing left
            # Check for objects
            if gameBoard[headLocation["y"]][headLocation["x"] - 1] == 3 or gameBoard[headLocation["y"]][headLocation["x"] - 1] == 2:  # Wall
                gameOver = True
                print("Game over!")
                return
            elif gameBoard[headLocation["y"]][headLocation["x"] - 1] == 4:  # Apple
                score += 100
                print("Yummy!")
                if not timeTillNextTick <= 0.1:
                    timeTillNextTick -= 0.025
            headLocation["x"] -= 1
            # Replace new head location with a head block
            gameBoard[headLocation["y"]][headLocation["x"]] = 1


class Graphics:
    def __init__(self):
        pass

    @staticmethod
    def render():
        screen.blit(background, (0, 0))
        pygame.display.flip()

    @staticmethod
    def printText(txt, x, y, size, color):
        # Display some text
        font = pygame.font.Font(None, size)
        text = font.render(txt, True, color)
        textpos = text.get_rect()
        textpos.x = x
        textpos.y = y
        background.blit(text, textpos)


def graphicsThread():
    global gameOver, timeTillNextTick, timer, score
    while True:
        if not gameOver:
            milli = clock.tick()
            seconds = milli / 1000
            timer += seconds
            Snake.draw()
            Graphics.printText(str("Score:" + str(score+(math.ceil(timer)))), 25, 5, 25, (255, 255, 0))
            Graphics.render()
            # print(round(timer*100)/100)
            if (round(timer*100)/100) > timeTillNextTick:
                Snake.processBody()
            time.sleep(timeTillNextTick)
        else:
            break


if __name__ == '__main__':
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snek")

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Run main thread
    Snake.spawnMatrix(32, 24)  # Generate game matrix
    Snake.spawnRandApples(5)  # Spawn initial apples
    Snake.spawnSnake(5)  # Generate the snake

    # Spawn graphics thread
    gfxThread = threading.Thread(target=graphicsThread)
    gfxThread.start()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[ i ] Exiting... Goodbye!")
                gameOver = True
                gfxThread.join()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Register key input
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if snakeDirection == 0 or snakeDirection == 1:
                        snakeDirection = 3
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if snakeDirection == 0 or snakeDirection == 1:
                        snakeDirection = 2
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if snakeDirection == 2 or snakeDirection == 3:
                        snakeDirection = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if snakeDirection == 2 or snakeDirection == 3:
                        snakeDirection = 1
