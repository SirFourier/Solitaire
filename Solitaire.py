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

# card class containing image, position, size data
class Card:
    # set global card attributes
    size = width, height = 95, 140
    imagePath = "PNG-cards"
    suits = ("clubs", "diamonds", "hearts", "spades")

    # set cardback image
    cardback = loadImage(f"{imagePath}/cardback.png", size)

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.image = loadImage(f"{Card.imagePath}/{number}_of_{suit}.png", Card.size)
        self.rect = self.image.get_rect()
        self.faceUp = True
        self.draggable = True
        
    def draw(self, screen):
        # draws image onto rect surface
        screen.blit(self.image, self.rect)

# pile class containing cards
class Pile:
    # pile spacing for where to place them on the screen
    cardSpacing = 36
    pileSpacing = 120

    def __init__(self, pile):
        self.pile = pile 
        
    def handleMouseDown(self, movingPile):
        # check is cursor is inside card
        mouseX, mouseY = pygame.mouse.get_pos()

        # check if cursor is inside any of the cards in the pile
        for index, card in reversed(list(enumerate(self.pile))):
            # assume true to begin with
            inside = True

            if mouseX < card.rect.x or mouseX > card.rect.x + card.rect.w:
                inside = False
            elif mouseY < card.rect.y or mouseY > card.rect.y + card.rect.h: 
                inside = False

            if inside: 
                # partition pile into moving pile
                movingPile.pile = self.pile[index:]
                self.pile = self.pile[:index]
                movingPile.previousPile = self.pile
                
                movingPile.prevMouseX = mouseX
                movingPile.prevMouseY = mouseY
                break

    def draw(self, screen):
        for card in self.pile:
            card.draw(screen)


class MovingPile(Pile):
# When pile is being dragged by cursor

    def __init__(self):
        Pile.__init__(self, pile=[])
        self.prevMouseX = 0
        self.prevMouseY = 0
        self.previousPile = None

    def handleMouseMotion(self):
        # move card with cursor if held
        mouseX, mouseY = pygame.mouse.get_pos()

        for card in self.pile:
            # move card to new position based on previous and current mouse position
            card.rect.x += mouseX - self.prevMouseX  
            card.rect.y += mouseY - self.prevMouseY

        self.prevMouseX = mouseX
        self.prevMouseY = mouseY

    def handleMouseUp(self):
        
        # if no new pile selected, return moving pile to previous pile
        for index, card in enumerate(self.pile):
            card.rect.x = self.previousPile[-1].rect.x
            card.rect.y = self.previousPile[-1].rect.y + Pile.cardSpacing
            self.previousPile.append(card)

        # reset held card/pile held
        self.pile = []

# set screen properties
screenSize = width, height = 1100, 800
darkGreen = 50, 122, 14 # for background

# create deck
deck = []
for suit in Card.suits:
    # 1 = ace, 11 = jack, 12 = queen, 13 = king
    for number in range(1, 14):
        deck.append(Card(number, suit))

# shuffle deck
random.shuffle(deck)

# create 7 piles from shuffled deck
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
        cardPosition[1] += Pile.cardSpacing 

    piles.append(Pile(pile))
    # move position of next pile in the x direction
    cardPosition[0] += Pile.pileSpacing
    # reset y position of pile
    cardPosition[1] = startingCardPosition[1]

# create a moving pile (intially empty)
movingPile = MovingPile()

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
                pile.handleMouseDown(movingPile)

        if event.type == pygame.MOUSEMOTION and movingPile.pile:
            movingPile.handleMouseMotion()

        if event.type == pygame.MOUSEBUTTONUP and movingPile.pile:
            movingPile.handleMouseUp()

    # render
    screen.fill(darkGreen)
    for pile in piles:
        pile.draw(screen)
    movingPile.draw(screen)
    pygame.display.flip()

    # maintain 60 fps
    clock.tick(60)

