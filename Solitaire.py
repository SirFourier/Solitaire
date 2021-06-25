# Solitaire Game
# Source of card images: https://code.google.com/archive/p/vector-playing-deck/
import sys
import pygame
import random

# initialise pygame
pygame.init()

# load and scale image to new size
def loadImage(path, newSize=None):
    image = pygame.image.load(path)
    if newSize:
        image = pygame.transform.scale(image, newSize)
    return image

# card class containing image, position, and game data
class Card:
    # keep track of which card is held by the cursor and previous mouse position
    held = None
    prevMouseX = 0
    prevMouseY = 0

    # cardback image
    cardback = None

    def __init__(self, number, suit, image):
        self.number = number
        self.suit = suit
        self.image = image
        self.rect = image.get_rect()
        self.faceUp = True
        self.draggable = True

    def handleMouseDown(self):
        # check is cursor is inside card
        mouseX, mouseY = pygame.mouse.get_pos()
        # assume true to begin with
        isInside = True

        if mouseX < self.rect.x or mouseX > self.rect.x + self.rect.w:
            isInside = False
        elif mouseY < self.rect.y or mouseY > self.rect.y + self.rect.h: 
            isInside = False

        # set held card to this card if cursor is inside
        if isInside: 
            Card.held = self
            Card.prevMouseX = mouseX
            Card.prevMouseY = mouseY

    def handleMouseMotion(self):
        # move card with cursor if held
        mouseX, mouseY = pygame.mouse.get_pos()
        # move card to new position based on previous and current mouse position
        self.rect.x = self.rect.x + mouseX - Card.prevMouseX  
        self.rect.y = self.rect.y + mouseY - Card.prevMouseY
        Card.prevMouseX = mouseX
        Card.prevMouseY = mouseY 

    def handleMouseUp(self):
        Card.held = None

    def draw(self, screen):
        # draws image onto rect surface
        screen.blit(self.image, self.rect)


class Pile:

    def __init__(self):
        pass


# set screen properties
screenSize = width, height = 1100, 800
darkGreen = 50, 122, 14 # for background

# set card properties
cardSize = width, height = 95, 140
imagePath = "PNG-cards"
suits = ("clubs", "diamonds", "hearts", "spades")
deck = []

# create deck
for suit in suits:
    # 1 = ace, 11 = jack, 12 = queen, 13 = king
    for number in range(1, 14):
        image = loadImage(f"{imagePath}/{number}_of_{suit}.png", cardSize)
        deck.append(Card(number, suit, image))

# set cardback image
Card.cardback = loadImage(f"{imagePath}/cardback.png", cardSize)

# shuffle deck
random.shuffle(deck)

# remove cards from deck and add to piles

# create 7 piles
cardSpacing = 36
pileSpacing = 120
piles = []
startingCardPosition = [100, 100]
cardPosition = startingCardPosition.copy()
for _ in range(7):
    pile = []
    for _ in range(5):
        card = deck.pop()
        card.rect.x, card.rect.y = cardPosition
        pile.append(card)
        # move position of next card in the y direction
        cardPosition[1] += cardSpacing 
    
    piles.append(pile)
    # move position of next pile in the x direction
    cardPosition[0] += pileSpacing
    # reset y position of pile
    cardPosition[1] = startingCardPosition[1]

# set screen and clock
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for pile in piles:
                for card in pile:
                    if card.draggable: 
                        card.handleMouseDown()
        if event.type == pygame.MOUSEMOTION and Card.held:
            Card.held.handleMouseMotion()
        if event.type == pygame.MOUSEBUTTONUP and Card.held:
            Card.held.handleMouseUp()

    # Draw all assets
    screen.fill(darkGreen)
    for pile in piles:
        for card in pile:
            card.draw(screen)
    pygame.display.flip()

    clock.tick(60)

