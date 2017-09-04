import pygame

SCREEN_SIZE = [1600, 1200]

class Custom_Event:
    UPDATE_TEMP_MESSAGE         =   pygame.USEREVENT
    UPDATE_GRAPH_MESSAGE        =   pygame.USEREVENT + 1
    UPDATE_INPUT_MESSAGE        =   pygame.USEREVENT + 2
    DRAW_CIRCLES                =   pygame.USEREVENT + 3
    RUN_COMMAND                 =   pygame.USEREVENT + 4
    UPDATE_GRAPH_STATE          =   pygame.USEREVENT + 5
    UPDATE_TEMP_MESSAGE_TIME    =   pygame.USEREVENT + 6

class Graph_State:
    NFA     =   "NFA"
    PDA     =   "PDA"
    DFA     =   "DFA"

class Color:
    BLACK       =   (  0,   0,   0)
    WHITE       =   (255, 255, 255)
    BLUE        =   (  0,   0, 255)
    GREEN       =   (  0, 120,   0)
    RED         =   (255,   0,   0)
    GREY        =   (130, 130, 130)
    LIGHT_GREY  =   (190, 190, 190)

class Token:
    AND     =   "."
    OR      =   "+"
    KLEENE  =   "*"
    EPSILON =   "*"
    STACK   =   '$'

class Pivot:
    CENTER = 0.5

    LEFT = 0
    RIGHT = 1.0

    TOP = 0
    BOTTOM = 1.0
