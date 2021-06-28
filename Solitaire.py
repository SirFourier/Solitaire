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
        self.colour = Card.getColour(suit)
        self.image = loadImage(f"{Card.imagePath}/{number}_of_{suit}.png", Card.size)
        self.rect = self.image.get_rect()
        self.faceUp = False
        
    @staticmethod
    def getColour(suit):
        if suit == "clubs" or suit == "spades":
            return "black"
        return "red"

    @staticmethod    
    def oppositeColour(card1, card2):
        # return true if the two cards have opposite colours
        if card1.colour == card2.colour:
            return False
        return True

    @staticmethod
    def validNumber(card1, card2):
        # return true if card 2 is valued 1 less than card 1
        if card2.number == card1.number - 1:
            return True
        return False

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

    # set empty pile slot
    emptyPileSlotImage = loadImage(f"{Card.imagePath}/empty_pile_slot.png", Card.size)

    def __init__(self, pile=[], posX=0, posY=0):
        self.posX = posX
        self.posY = posY
        self.pile = pile 

    def update(self):
        # update positions of the cards
        for index, card in enumerate(self.pile):
            card.rect.x = self.posX
            card.rect.y = self.posY + Pile.cardSpacing * index

    def draw(self, screen):
        # if pile is exists
        if self.pile:
            # draw cards
            for card in self.pile:
                card.draw(screen)
        else: 
            # draw empty pile slot
            rect = pygame.Rect(self.posX, self.posY, Card.size[0], Card.size[1])
            screen.blit(Pile.emptyPileSlotImage, rect)


# When pile is being dragged by cursor
class MovingPile(Pile):
    # inherit pile class
    def __init__(self):
        Pile.__init__(self)
        # keep track of mouse positions
        self.prevMouseX = 0
        self.prevMouseY = 0
        # keep track of previous pile object
        self.previousPile = None

    def handleMouseDown(self, pile):
        # get current mouse position
        mouseX, mouseY = pygame.mouse.get_pos()

        # check if cursor is inside any of the cards in the pile (starting from last card)
        for index, card in reversed(list(enumerate(pile.pile))):
            # if mouse is inside card
            if card.rect.collidepoint(mouseX, mouseY) and card.faceUp: 
                # partition pile into moving pile
                self.pile = pile.pile[index:]
                pile.pile = pile.pile[:index]
                self.previousPile = pile
                
                # set moving pile position to the card
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

    def handleMouseUp(self, piles):
        # if no pile selected, return moving pile to previous 
        pileSelected = False
        
        # check if valid pile
        for pile in piles: 
            if pile.pile:
                # check if pile overlaps with card
                if self.pile[0].rect.colliderect(pile.pile[-1].rect):
                    # check if opposite colours
                    if Card.oppositeColour(self.pile[0], pile.pile[-1]):
                        # check if last card of stationary pile is valued 1 more
                        if Card.validNumber(pile.pile[-1], self.pile[0]):
                            # Extend the stationary pile with the moving pile
                            pile.pile.extend(self.pile)
                            pile.update()
                            pileSelected = True

                            # if there is a pile in the previous pile
                            if self.previousPile.pile:
                                # flip the last card face up
                                self.previousPile.pile[-1].faceUp = True

                            break

        if not pileSelected:
            # return the moving pile to the previous pile
            self.previousPile.pile.extend(self.pile)
            self.previousPile.update()
        
        # clear held card/pile held
        self.pile.clear()

    def draw(self, screen):
        # create seperate draw method to avoid drawing empty card slot
        if self.pile:
            Pile.draw(self, screen)

# Contains the remaining cards after setting up the tableau
class StockPile(Pile):

    def update(self):
        # update positions of the cards
        for card in self.pile:
            card.faceUp = False
            card.rect.x = self.posX
            card.rect.y = self.posY

# Contains the card(s) pulled from the stock
class WastePile(Pile):

    def handleMouseDown(self, stockPile):
        # get mouse position
        mouseX, mouseY = pygame.mouse.get_pos()
        
        if stockPile.pile:
            if stockPile.pile[-1].rect.collidepoint(mouseX, mouseY): 
                # move top card into waste pile
                self.pile.append(stockPile.pile.pop())
                self.pile[-1].faceUp = True
                self.update()

                # track position of mouse
                self.prevMouseX = mouseX
                self.prevMouseY = mouseY
        else:
            # return waste pile to stock pile
            self.pile.reverse()
            stockPile.pile = self.pile.copy()
            self.pile.clear()

            stockPile.update()
            self.update()

    def update(self):
        # update positions of the cards
        for card in self.pile:
            card.rect.x = self.posX
            card.rect.y = self.posY


class FoundationPile(Pile):
    pass

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

# place remining cards in stock pile
stockPile = StockPile(deck)
stockPile.update()

# create a pile to place cards pulled from the stock (initially empty)
wastePile = WastePile([], 0, 200)

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
            wastePile.handleMouseDown(stockPile)
            for pile in piles:
                movingPile.handleMouseDown(pile)
            movingPile.handleMouseDown(wastePile)

        if event.type == pygame.MOUSEMOTION and movingPile.pile:
            movingPile.handleMouseMotion()

        if event.type == pygame.MOUSEBUTTONUP and movingPile.pile:
            movingPile.handleMouseUp(piles)

    # render
    screen.fill(darkGreen)
    for pile in piles:
        pile.draw(screen)
    stockPile.draw(screen)
    wastePile.draw(screen)
    movingPile.draw(screen)
    pygame.display.flip()

    # maintain 60 fps
    clock.tick(60)

