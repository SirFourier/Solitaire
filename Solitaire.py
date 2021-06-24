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

    def draw(self, screen):
        # draws image onto rect surface
        screen.blit(self.image, self.rect)

# set card properties
size = width, height = 1300, 750
cardSize = width, height = 110, 160
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

cards[50].rect.x, cards[50].rect.y = 700, 500
cards[5].rect.x, cards[5].rect.y = 200, 500
cards[5].image = Card.cardback

# main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            cards[51].handleMouseDown()
            cards[50].handleMouseDown()
            cards[5].handleMouseDown()
        if event.type == pygame.MOUSEMOTION and Card.held:
            Card.held.handleMouseMotion()
        if event.type == pygame.MOUSEBUTTONUP and Card.held:
            Card.held = None

    # Handle mouse left click events
    screen.fill(darkGreen)
    cards[51].draw(screen)
    cards[50].draw(screen)
    cards[5].draw(screen)
    pygame.display.flip()

    clock.tick(60)

