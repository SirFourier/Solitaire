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

# card class containing image, position, and size data
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

    def __init__(self, pile, posX, posY):
        self.posX = posX
        self.posY = posY
        self.pile = pile 

    def update(self):
        # update positions of the cards based on the first card
        for index, card in enumerate(self.pile):
            card.rect.x = self.posX
            card.rect.y = self.posY + Pile.cardSpacing * index

    def draw(self, screen):
        for card in self.pile:
            card.draw(screen)


class MovingPile(Pile):
# When pile is being dragged by cursor

    def __init__(self):
        Pile.__init__(self, pile=[], posX=0, posY=0)
        self.prevMouseX = 0
        self.prevMouseY = 0
        self.previousPile = None

    def handleMouseDown(self, pile):
        # check is cursor is inside card
        mouseX, mouseY = pygame.mouse.get_pos()

        # check if cursor is inside any of the cards in the pile
        for index, card in reversed(list(enumerate(pile.pile))):
            
            # if mouse is inside card
            if card.rect.collidepoint(mouseX, mouseY): 
                # partition pile into moving pile
                self.pile = pile.pile[index:]
                pile.pile = pile.pile[:index]
                self.previousPile = pile
                
                self.prevMouseX = mouseX
                self.prevMouseY = mouseY
                return

    def handleMouseMotion(self):
        # move card with cursor if held
        mouseX, mouseY = pygame.mouse.get_pos()

        for card in self.pile:
            # move card to new position based on previous and current mouse position
            card.rect.move_ip(mouseX - self.prevMouseX, mouseY - self.prevMouseY)

        self.prevMouseX = mouseX
        self.prevMouseY = mouseY

    def handleMouseUp(self):
        # if no new pile selected, return moving pile to previous pile
        self.previousPile.pile.extend(self.pile)
        self.previousPile.update()
        
        # reset held card/pile held
        self.pile.clear()

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
pilePosX = 100
pilePosY = 100
for _ in range(7):
    newPile = Pile([], pilePosX, pilePosY)
    for _ in range(5):
        card = deck.pop()
        newPile.pile.append(card)

    # update positions of cards based on position of the pile
    newPile.update()
    piles.append(newPile)

    # move position of next pile in the x direction
    pilePosX += Pile.pileSpacing

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
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for pile in piles:
                movingPile.handleMouseDown(pile)

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

