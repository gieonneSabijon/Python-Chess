import pygame
import Piece
from pygame.locals import *



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Python-Chess')


    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    currentGame = Piece.gameInfo()
    board=[]
    for i in reversed(range(8)): #row
        row = []
        for j in range (8): #column
            row.append(Piece.Position(j, i))
        
        board.append(row)

    blackList = pieceSetup("BLACK", currentGame)
    whiteList = pieceSetup("WHITE", currentGame)

    currentGame.setGame(board, whiteList, blackList, [])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False 
        draw(screen, currentGame)
        pygame.display.flip()

    pygame.quit()

def draw(surface, gameinfo):
    black = Color(40,45,54)

    whitePawnImage = pygame.image.load('Assets/White Pawn.png')
    blackPawnImage = pygame.image.load('Assets/Black Pawn.png')
    whiteRookImage = pygame.image.load('Assets/White Rook.png')
    blackRookImage = pygame.image.load('Assets/Black Rook.png')

    pieceRect = whitePawnImage.get_rect()
    pieceImage = None

    for i in reversed(range(8)):
        for j in range(8):
            tile = Rect(j * 64, i * 64, 64, 64)
            if (i + j) % 2 != 0:
                pygame.draw.rect(surface, black, tile)

    for i in (gameinfo.whiteList + gameinfo.blackList):
        pieceRect.topleft = (i.x * 64, 448 - i.y * 64)
        if isinstance(i, Piece.Pawn):
            if i.side == "WHITE":
                pieceImage = whitePawnImage
            else:
                pieceImage = blackPawnImage
        elif isinstance(i, Piece.Rook):
            if i.side == "WHITE":
                pieceImage = whiteRookImage
            else:
                pieceImage = blackRookImage

        if pieceImage:
            surface.blit(pieceImage, pieceRect)
        
def pieceSetup(side, gameinfo):
    pieces = []
    pawnY = 0
    pieceY = 0
    if side == "WHITE":
        pawnY = 1
        pieceY = 0
    else:
        pawnY = 6
        pieceY = 7

    for i in range(8):
        pieces.append(Piece.Pawn(side, i, pawnY, gameinfo))

    pieces.append(Piece.Rook(side, 0, pieceY, gameinfo))
    pieces.append(Piece.Rook(side, 7, pieceY, gameinfo))

    return pieces
    






if __name__ == '__main__': main()