import pygame, element
from constants import Color, Pivot, SCREEN_SIZE
from constants import Custom_Event as ce

EVENT_LIST = [ce.UPDATE_TEMP_MESSAGE,
    ce.UPDATE_TEMP_MESSAGE_TIME,
    ce.UPDATE_GRAPH_MESSAGE,
    ce.UPDATE_INPUT_MESSAGE,
    ce.DRAW_CIRCLES]

CLOCK = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("Graphs v1.0")
screen = pygame.display.set_mode(SCREEN_SIZE)

graph_state = element.Message()
input_message = element.Message(pivot=(Pivot.RIGHT, Pivot.BOTTOM))
temp_message = element.Temp_Message(size=60, pivot=(Pivot.CENTER, Pivot.BOTTOM))

circles = []

def update():
    for event in pygame.event.get(EVENT_LIST):
        if event.type == ce.UPDATE_TEMP_MESSAGE:
            temp_message.update(event.message)
        if event.type == ce.UPDATE_TEMP_MESSAGE_TIME:
            temp_message.update(event.message, event.time)
        if event.type == ce.UPDATE_INPUT_MESSAGE:
            input_message.update(event.message)
        if event.type == ce.UPDATE_GRAPH_MESSAGE:
            graph_state.update(event.message)
        if event.type == ce.DRAW_CIRCLES:
            global circles
            circles = event.circles

def draw():
    CLOCK.tick(60)
    screen.fill(Color.GREY)

    graph_state.draw(screen)
    input_message.draw(screen, SCREEN_SIZE)
    temp_message.draw(screen, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]))

    for circle in circles:
        for line in circle.lines:
            line.draw(screen)
    for circle in circles:
        circle.draw(screen)

    pygame.display.flip()
