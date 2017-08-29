import pygame, visuals, logic

DONE = False

#Allows only the events that will actually be used
pygame.event.set_allowed(None)
pygame.event.set_allowed(visuals.EVENT_LIST + logic.EVENT_LIST + [pygame.QUIT])

logic.init()

while not DONE:
    for e in pygame.event.get(pygame.QUIT):
        DONE = True

    logic.update()

    visuals.update()

    visuals.draw()
