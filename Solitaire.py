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
    
def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

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
    for number in range(1, 14):
        cards.append(Card(number, suit, cardSize))


screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while 1:
    handleEvents()

    screen.fill(black)
    screen.blit(cards[51].image, cards[51].rect)
    pygame.display.flip()

    clock.tick(60)

#test commit