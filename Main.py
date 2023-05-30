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
    for i in range(8): #row
        row = []
        for j in range (8): #column
            row.append(Piece.Position(j, i))
        
        board.append(row)
    kings = []
    blackList = pieceSetup("BLACK", currentGame)
    whiteList = pieceSetup("WHITE", currentGame)
    for team in [whiteList, blackList]:
        for piece in team:
            if isinstance(piece, Piece.King):
                kings.append(piece)
                break

    
    
    currentGame.setGame(board, whiteList, blackList, [])
    selectedPiece = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT: #Exit Game
                running = False 

            if event.type == pygame.MOUSEBUTTONUP:
                if selectedPiece and len(currentGame.moveset) > 0:
                    for move in currentGame.moveset:
                        tempRect = Rect(move.x * 64, 448 - move.y * 64, 64, 64)
                        if tempRect.collidepoint(event.pos):
                            selectedPiece.move(move)
                            break
                for row in currentGame.board:
                    for cell in row:
                        tempRect = Rect(cell.x * 64, 448 - cell.y * 64, 64, 64)
                        if tempRect.collidepoint(event.pos):
                            selectedPiece = cell.isOccupied(currentGame.blackList + currentGame.whiteList)
                            break
                        else:
                            selectedPiece = None
                            currentGame.moveset = []
                    else:
                        continue
                    break
                
        
        if selectedPiece:
            currentGame.moveset = selectedPiece.getMoveset()
        
        print(f'White King: {kings[0].isInCheckmate()}')
        print(f'Black King: {kings[1].isInCheckmate()}')
        
        pygame.display.flip()
        draw(screen, currentGame)

    pygame.quit()

def draw(surface, gameinfo):
    black = Color(40,45,54)

    whitePawnImage = pygame.image.load('Assets/White Pawn.png')
    blackPawnImage = pygame.image.load('Assets/Black Pawn.png')
    whiteRookImage = pygame.image.load('Assets/White Rook.png')
    blackRookImage = pygame.image.load('Assets/Black Rook.png')
    whiteBishopImage = pygame.image.load('Assets/White Bishop.png')
    blackBishopImage = pygame.image.load('Assets/Black Bishop.png')
    whiteKnightImage = pygame.image.load('Assets/White Knight.png')
    blackKnightImage = pygame.image.load('Assets/Black Knight.png')
    whiteQueenImage = pygame.image.load('Assets/White Queen.png')
    blackQueenImage = pygame.image.load('Assets/Black Queen.png')
    whiteKingImage = pygame.image.load('Assets/White King.png')
    blackKingImage = pygame.image.load('Assets/Black King.png')

    pieceRect = whitePawnImage.get_rect()
    pieceImage = None

    for i in reversed(range(8)):
        for j in range(8):
            tile = Rect(j * 64, i * 64, 64, 64)
            if (i + j) % 2 != 0:
                pygame.draw.rect(surface, black, tile)
            else:
                pygame.draw.rect(surface, (255, 255, 255), tile)
    
    for move in gameinfo.moveset:
        moveRect = Rect(move.x * 64, 448 - move.y * 64, 64, 64)
        pygame.draw.rect(surface, (0, 255, 0), moveRect, 5)

    for i in (gameinfo.whiteList + gameinfo.blackList):
        pieceRect.topleft = (i.x * 64, 448 - i.y * 64)

        for piece, image in zip([Piece.Pawn, Piece.Rook, Piece.Bishop, Piece.Knight, Piece.Queen, Piece.King], 
                                    [(whitePawnImage, blackPawnImage),
                                    (whiteRookImage, blackRookImage),
                                    (whiteBishopImage, blackBishopImage),
                                    (whiteKnightImage, blackKnightImage), 
                                    (whiteQueenImage, blackQueenImage),
                                    (whiteKingImage, blackKingImage)]):
            

            
            if isinstance(i, piece):
                if i.side == "WHITE":
                    pieceImage = image[0]
                else:
                    pieceImage = image[1]

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
    pieces.append(Piece.Bishop(side, 2, pieceY, gameinfo))
    pieces.append(Piece.Bishop(side, 5, pieceY, gameinfo))
    pieces.append(Piece.Knight(side, 1, pieceY, gameinfo))
    pieces.append(Piece.Knight(side, 6, pieceY, gameinfo))
    pieces.append(Piece.Queen(side, 3, pieceY, gameinfo))
    pieces.append(Piece.King(side, 4, pieceY, gameinfo))
    return pieces
    






if __name__ == '__main__': main()