# Solitaire Game
# Source of card images: https://code.google.com/archive/p/vector-playing-cards/

import sys
import pygame

# create instance for each card holding image and position data
class Card:

    def __init__(self, number, suit, cardSize):
        self.number = number
        self.suit = suit
        self.image = pygame.image.load(f"./PNG-cards/{number}_of_{suit}.png")
        self.image = pygame.transform.scale(self.image, cardSize)
        self.rect = self.image.get_rect()

    def handleLeftClick(self):
        # check is cursor is inside card
        mouseX, mouseY = pygame.mouse.get_pos()
        isInside = True

        if mouseX < self.rect.x or mouseX > self.rect.x + self.rect.w:
            isInside = False
        elif mouseY < self.rect.y or mouseY > self.rect.y + self.rect.h: 
            isInside = False

        if isInside:
            self.rect.x = mouseX - 0.5 * self.rect.w
            self.rect.y = mouseY - 0.5 * self.rect.h
        

# initialise pygame
pygame.init()

# set card properties
size = width, height = 1300, 750
cardSize = width, height = 110, 160
black = 0, 0, 0
suits = ("clubs", "diamonds", "hearts", "spades")
cards = []

# create cards
for suit in suits:
    # 1 = ace, 11 = jack, 12 = queen, 13 = king
    for number in range(1, 14):
        cards.append(Card(number, suit, cardSize))


# set screen and clock
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# main game loop
while 1:

    # Handle exit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
    
    # Handle mouse left click events
    if pygame.mouse.get_pressed() == (1, 0, 0): 
        cards[51].handleLeftClick()

    screen.fill(black)
    screen.blit(cards[51].image, cards[51].rect)
    pygame.display.flip()

    clock.tick(60)

