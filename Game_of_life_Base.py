import pygame
import time
import numpy as np

try:
    import pygame_sdl2

    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

pygame.init()

width, height = 700, 700

screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = 60, 60

dimCW = width / nxC
dimCH = height / nyC

gameState = np.zeros((nxC, nyC))

posInitX = int((nxC / 2) - 3)
posInitY = int((nyC / 2) - 5)
gameState[posInitX, posInitY] = 1

pauseExec = True

endGame = False

while not endGame:

    newGameState = np.copy(gameState)

    screen.fill(bg)

    time.sleep(0.1)

    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            endGame = True
            break

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                endGame = True
                break

            if event.key == pygame.K_r:
                gameState = np.zeros((nxC, nyC))
                newGameState = np.zeros((nxC, nyC))
                pauseExec = True
            else:
                pauseExec = not pauseExec

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:

            if mouseClick[1]:

                pauseExec = not pauseExec

            else:

                posX, posY, = pygame.mouse.get_pos()

                celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

                newGameState[celX, celY] = not gameState[celX, celY]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExec:

                n_neigh = (
                        gameState[(x - 1) % nxC, (y - 1) % nyC]
                        + gameState[x % nxC, (y - 1) % nyC]
                        + gameState[(x + 1) % nxC, (y - 1) % nyC]
                        + gameState[(x - 1) % nxC, y % nyC]
                        + gameState[(x + 1) % nxC, y % nyC]
                        + gameState[(x - 1) % nxC, (y + 1) % nyC]
                        + gameState[x % nxC, (y + 1) % nyC]
                        + gameState[(x + 1) % nxC, (y + 1) % nyC]
                )

                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            poly = [
                (int(x * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int(y * dimCH)),
                (int((x + 1) * dimCW), int((y + 1) * dimCH)),
                (int(x * dimCW), int((y + 1) * dimCH)),
            ]

            if newGameState[x, y] == 0:

                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pauseExec:

                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:

                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    gameState = np.copy(newGameState)

    pygame.display.flip()
