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

# ----------------creating card and pile classes--------------------#
# card class containing image, position, and size data
class Card:
    # set global card attributes
    size = width, height = 95, 140
    imagePath = "PNG-cards"
    suits = ("clubs", "diamonds", "hearts", "spades")

    # set cardback image
    cardbackImage = loadImage(f"{imagePath}/cardback.png", size)

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
        self.image = loadImage(f"{Card.imagePath}/{number}_of_{suit}.png", Card.size)
        self.rect = self.image.get_rect()
        self.faceUp = False
        self.draggable = False
        
    def draw(self, screen):
        # draws image or cardback depending if face up or not
        image = self.cardbackImage
        if self.faceUp:
            image = self.image
        screen.blit(image, self.rect)

# pile class containing cards
class Pile:
    # pile spacing for where to place them on the screen
    cardSpacing = 36
    pileSpacing = 140

    def __init__(self, pile, posX, posY):
        self.posX = posX
        self.posY = posY
        self.pile = pile 

    def update(self):
        # update positions of the cards
        for index, card in enumerate(self.pile):
            card.rect.x = self.posX
            card.rect.y = self.posY + Pile.cardSpacing * index

    def draw(self, screen):
        for card in self.pile:
            card.draw(screen)

# When pile is being dragged by cursor
class MovingPile(Pile):
    # inherit pile class
    def __init__(self):
        Pile.__init__(self, pile=[], posX=0, posY=0)
        # keep track of mouse positions
        self.prevMouseX = 0
        self.prevMouseY = 0
        # keep track of previous pile object
        self.previousPile = None

    def handleMouseDown(self, pile):
        # check is cursor is inside card
        mouseX, mouseY = pygame.mouse.get_pos()

        # check if cursor is inside any of the cards in the pile (starting from last card)
        for index, card in reversed(list(enumerate(pile.pile))):
            # if mouse is inside card
            if card.rect.collidepoint(mouseX, mouseY) and card.draggable: 
                # partition pile into moving pile
                self.pile = pile.pile[index:]
                pile.pile = pile.pile[:index]
                self.previousPile = pile
                
                # set moving pile position to the same as the card
                self.posX = card.rect.x
                self.posY = card.rect.y

                # track position of mouse
                self.prevMouseX = mouseX
                self.prevMouseY = mouseY

                return

    def handleMouseMotion(self):
        # move card with cursor if held
        mouseX, mouseY = pygame.mouse.get_pos()
        
        # move pile based on previous position of mouse
        self.posX += mouseX - self.prevMouseX
        self.posY += mouseY - self.prevMouseY
        self.update()

        self.prevMouseX = mouseX
        self.prevMouseY = mouseY

    def handleMouseUp(self):
        # if no new pile selected, return moving pile to previous pile
        self.previousPile.pile.extend(self.pile)
        self.previousPile.update()
        
        # clear held card/pile held
        self.pile.clear()

# ------------------------set screen properties--------------------------#
screenSize = width, height = 1100, 800
darkGreen = 50, 122, 14 # for background

# ---------------------------setting up deck-----------------------------#
# create deck
deck = []
for suit in Card.suits:
    # 1 = ace, 11 = jack, 12 = queen, 13 = king
    for number in range(1, 14):
        deck.append(Card(number, suit))

# shuffle deck
random.shuffle(deck)

# ----------------------setting up the tableau-------------------------#
# create 7 piles from shuffled deck
piles = []
pilePosX = 80
pilePosY = 100
numberOfPiles = 7
numberOfCards = 1
for pileNumber in range(numberOfPiles):
    # keep track of how many face downs have been placed
    faceDownCounter = 0
    # create new pile object
    newPile = Pile([], pilePosX, pilePosY)

    # iterate through pile of cards
    for cardNumber in range(numberOfCards):
        card = deck.pop()

        # turn card face up if card number is greater or equal to pile number
        if cardNumber >= pileNumber:
            card.faceUp = True
            card.draggable = True
        
        newPile.pile.append(card)

    # update positions of cards based on position of the pile
    newPile.update()
    piles.append(newPile)

    # move position of next pile in the x direction
    pilePosX += Pile.pileSpacing

    # next pile has 1 more card
    numberOfCards += 1

# create a moving pile (intially empty)
movingPile = MovingPile()

# set screen and clock
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

# ---------------------------main game loop------------------------------#
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

