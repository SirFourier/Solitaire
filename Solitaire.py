# Solitaire Game
# Source of card images: https://code.google.com/archive/p/vector-playing-cards/
import sys
import pygame

# initialise pygame
pygame.init()

# load and scale image to new size
def loadImage(path, size):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
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
        self.rect = self.image.get_rect()
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

        # set held is true if inside
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

    def handleMouseUp(self, pile):
        # check the last card of each pile
        # if near a valid card, attach to it
        if self.rect.x < pile[-2].rect.x + 0.5 * pile[-2].rect.w and self.rect.x > pile[-2].rect.x - 0.5 * pile[-2].rect.w: 
            if self.rect.y < pile[-2].rect.y + 0.5 * pile[-2].rect.h and self.rect.y > pile[-2].rect.y - 0.5 * pile[-2].rect.h: 
                self.rect.x = pile[-2].rect.x
                self.rect.y = pile[-2].rect.y + 40

        Card.held = None

    def draw(self, screen):
        # draws image onto rect surface
        screen.blit(self.image, self.rect)

# set card properties
size = width, height = 1300, 750
cardSize = width, height = 95, 140
darkGreen = 50, 122, 14
imagePath = "PNG-cards"
suits = ("clubs", "diamonds", "hearts", "spades")
cards = []

# create cards
for suit in suits:
    # 1 = ace, 11 = jack, 12 = queen, 13 = king
    for number in range(1, 14):
        image = loadImage(f"{imagePath}/{number}_of_{suit}.png", cardSize)
        cards.append(Card(number, suit, image))

# set cardback image
Card.cardback = loadImage(f"{imagePath}/cardback.png", cardSize)

# set screen and clock
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# testing
cards[50].rect.x, cards[50].rect.y = 700, 500
cards[24].rect.x, cards[24].rect.y = 300, 200
cards[5].rect.x, cards[5].rect.y = 200, 500

# pile test
pile = [cards[50], cards[5], cards[24]]

# main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in pile:
                if card.draggable: 
                    card.handleMouseDown()
        if event.type == pygame.MOUSEMOTION and Card.held:
            Card.held.handleMouseMotion()
        if event.type == pygame.MOUSEBUTTONUP and Card.held:
            Card.held.handleMouseUp(pile)

    # Draw all assets
    screen.fill(darkGreen)
    for card in pile:
        card.draw(screen)
    pygame.display.flip()

    clock.tick(60)

