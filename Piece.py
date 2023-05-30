from abc import ABC, abstractmethod

class gameInfo:
    @classmethod
    def setGame(cls, board, whiteList, blackList, graveyard):
        cls.board = board
        cls.whiteList = whiteList
        cls.blackList = blackList
        cls.graveyard = graveyard
        cls.moveset = []

    @classmethod
    def updateList(cls, side, pieceList):
        if side == "WHITE":
            cls.blackList = pieceList
        else:
            cls.whiteList = pieceList

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def isOccupied(self, pieceList):
        """Checks to see if there is currently a piece alive on that tile
        
        Keyword arguments:
        pieceList (List) -- list of piece objects
        Return: returns a piece from the piece list
        """
        
        for i in pieceList:
            if i.x == self.x and i.y == self.y:
                return i  
            
        return None 
    
    def __str__(self):
        return f"X: {self.x} Y: {self.y}"

class Piece(ABC): 

    @abstractmethod
    def __init__(self, side,x, y, gameinfo):
        self.side = side
        self.x = x
        self.y = y
        self.gameinfo = gameinfo

    @abstractmethod
    def move(self, option):
        """Move piece to the selected option from the available moveset
        
        Keyword arguments:
        option (position) -- a position object
        Return: return_description
        """
        pieceList = []

        if self.side == "WHITE":
            pieceList = self.gameinfo.blackList
        else:
            pieceList = self.gameinfo.whiteList

        enemy = option.isOccupied(pieceList)
        if enemy:
            pieceList.remove(enemy)
            self.gameinfo.graveyard.append(enemy)
            self.gameinfo.updateList(self.side, pieceList)

        self.x = option.x 
        self.y = option.y

    @abstractmethod
    def getMoveset(self): 
        pass
        

    def movesetFromList(current, posiions):
        moveset = []
        for i in posiions:
            for row in current.gameinfo.board:
                for cell in row:
                    if i.x == cell.x and i.y == cell.y:
                        nextPiece = i.isOccupied(current.gameinfo.blackList + current.gameinfo.whiteList)
                        if nextPiece:
                            if nextPiece.side == current.side:
                                continue
                        moveset.append(cell)
        return moveset
    
    def setRect(self, rect):
        self.rect = rect

    @abstractmethod
    def __str__(self):
        pass

class Pawn(Piece):
    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)
        self.firstMove = True

    def move(self, option):
        if option.x != self.x:
            pieceList = []

            if self.side == "WHITE":
                pieceList = self.gameinfo.blackList
            else:
                pieceList = self.gameinfo.whiteList

            enemy = option.isOccupied(pieceList)
            pieceList.remove(enemy)
            self.gameinfo.graveyard.append(enemy)
            self.gameinfo.updateList(self.side, pieceList)

        self.x = option.x 
        self.y = option.y

        self.firstMove = False
        

    def getMoveset(self):
        moveset = []
        yOffset = 0
        pieceList = []
        killLeft = None
        killRight = None
        if self.side == "WHITE":
            yOffset = 1
            pieceList = self.gameinfo.blackList
        else:
            yOffset = -1
            pieceList = self.gameinfo.whiteList

        if self.y + yOffset >= 0 and self.y + yOffset < 8:
            if not self.gameinfo.board[self.y + yOffset][self.x].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList):
                moveset.append(self.gameinfo.board[self.y + yOffset][self.x])
                

                if self.firstMove and not self.gameinfo.board[self.y + yOffset * 2][self.x].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList):
                    moveset.append(self.gameinfo.board[self.y + yOffset * 2][self.x])
            
            if self.x - 1 >= 0:
                killLeft = self.gameinfo.board[self.y + yOffset][self.x - 1].isOccupied(pieceList)
            if self.x + 1 < 8:
                killRight = self.gameinfo.board[self.y + yOffset][self.x + 1].isOccupied(pieceList)

            if killLeft:
                moveset.append(self.gameinfo.board[self.y + yOffset][self.x - 1])
            if killRight:
                moveset.append(self.gameinfo.board[self.y + yOffset][self.x + 1])
        #TODO add en passant
        return moveset
    
    def __str__(self):
        return f'{self.side} Pawn {self.gameinfo.board[self.y][self.x]}'
    
class Rook(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)
        self.firstMove = True

    def move(self, option):
        super().move(option)
        self.firstMove = False

    def getMoveset(self):
        moveset = []

        currentRow = self.gameinfo.board[self.y]
        
        leftSide = currentRow[:self.x]
        rightSide = currentRow[self.x + 1:]

        currentColumn = []

        for i in self.gameinfo.board:
            currentColumn.append(i[self.x])

        upSide = currentColumn[:self.y]
        downSide = currentColumn[self.y + 1:]

        searchList = [reversed(leftSide), rightSide, reversed(upSide), downSide]

        for i in searchList:
            for j in i:
                nextPiece = j.isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
                if nextPiece:
                    if nextPiece.side != self.side:
                        moveset.append(j)
                    break
                else:
                    moveset.append(j)

        return moveset
    
    def castle(self):
        if self.x == 0: 
            newX = 3
        else:
            newX = 5
        newPOS = Position(newX, self.y)
        self.move(newPOS)
            
    def __str__(self):
        return f'{self.side} Rook {self.gameinfo.board[self.y][self.x]}'

class Bishop(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)

    def move(self, option):
        return super().move(option)
    
    def getMoveset(self):
        moveset = []
        isBlocked = {'topLeft': False, 'topRight': False, 'bottomLeft': False, 'bottomRight': False}
        #top half
        for i, row in enumerate(self.gameinfo.board[self.y + 1:]):
            for key, pieceIndex in zip(['topLeft', 'topRight'], [(self.x + (-i - 1)), (self.x + (i + 1))]):
                if (pieceIndex < 0):
                    isBlocked['topLeft'] = True 
                if (pieceIndex > 7):
                    isBlocked['topRight'] = True

                if not isBlocked[key]:
                    nextPiece = row[pieceIndex].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
                    if nextPiece:
                        isBlocked[key] = True
                        if nextPiece.side != self.side:
                            moveset.append(row[pieceIndex])
                    else:
                        moveset.append(row[pieceIndex])

                

        #bottom half
        for i, row in enumerate(reversed(self.gameinfo.board[:self.y])):
            for key, pieceIndex in zip(['bottomLeft', 'bottomRight'], [self.x + (-i - 1), self.x + (i + 1)]):
                if (pieceIndex < 0):
                    isBlocked['bottomLeft'] = True 
                if (pieceIndex > 7):
                    isBlocked['bottomRight'] = True

                if not isBlocked[key]:
                    nextPiece = row[pieceIndex].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
                    if nextPiece:
                        isBlocked[key] = True
                        if nextPiece.side != self.side:
                            moveset.append(row[pieceIndex])
                    else:
                        moveset.append(row[pieceIndex])
                


        return moveset
    
    def __str__(self):
        return f'{self.side} Bishop {self.gameinfo.board[self.y][self.x]}'
    
class Queen(Piece):
    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)

    def move(self, option):
        super().move(option)

    def getMoveset(self):
        tempRook = Rook(self.side, self.x, self.y, self.gameinfo)
        tempBishop = Bishop(self.side, self.x, self.y, self.gameinfo)

        moveset = tempRook.getMoveset() + tempBishop.getMoveset()
        return moveset
    
    def __str__(self):
        return f'{self.side} Queen {self.gameinfo.board[self.y][self.x]}'
    
class Knight(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)

    def move(self, option):
        super().move(option)

    def getMoveset(self):
        movements = []
        for xOffset in [-2, -1, 1, 2]:
            for yOffset in [-2, -1, 1, 2]:
                if abs(xOffset) != abs(yOffset):
                    movements.append(Position(self.x + xOffset, self.y + yOffset))
        moveset = Piece.movesetFromList(self, movements)
        return moveset
    
    def __str__(self):
        return f'{self.side} Knight {self.gameinfo.board[self.y][self.x]}'

class King(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)
        self.firstMove = True
        self.attackers = []

    def move(self, option):
        if abs(option.x - self.x) > 1:
            if option.x == 2:
                rookObj = self.gameinfo.board[self.y][0].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
            else:
                rookObj = self.gameinfo.board[self.y][7].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)

            if rookObj:
                rookObj.castle()
        super().move(option)

        self.firstMove = False

    def getMoveset(self):
        self.attackers = []
        movements = []
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                if xOffset == 0 and yOffset == 0:
                    continue
                movements.append(Position(self.x + xOffset, self.y + yOffset))
        moveset = Piece.movesetFromList(self, movements)

        #Castling Logic
        if self.firstMove:
            currentRow = self.gameinfo.board[self.y]
            leftClear = True
            rightClear = True
            for i in range(1, 4):
                if currentRow[i].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList):
                    leftClear = False

            for i in range(5, 7):
                if currentRow[i].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList):
                    rightClear = False 
            
            leftRook = currentRow[0].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
            rightRook = currentRow[7].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
            if leftRook:
                if leftRook.firstMove and leftClear:
                    moveset.append(currentRow[2])
            if rightRook:
                if rightRook.firstMove and rightClear:
                    moveset.append(currentRow[6])

        enemyList = []
        if self.side == "WHITE":
            enemyList = self.gameinfo.blackList
        else:
            enemyList = self.gameinfo.whiteList

        for move in moveset:

            enemy = move.isOccupied(enemyList)
            if enemy:
                if isinstance(enemy, King):
                    moveset.remove(move)
                    continue

            tempKing = King(self.side, move.x, move.y, self.gameinfo)
            if tempKing.isInCheck():
                moveset.remove(move)
            

        return moveset
    
    def isInCheck(self):
        check = False
        enemyList = []
        enemyDict = {'queen': [], 'rook': [], 'bishop': [], 'knight': [], 'pawn': []}
        if self.side == "WHITE":
            enemyList = self.gameinfo.blackList
        else:
            enemyList = self.gameinfo.whiteList

        for piece in enemyList:
            if isinstance(piece, Queen):
                enemyDict['queen'].append(piece)
            elif isinstance(piece, Rook):
                enemyDict['rook'].append(piece)
            elif isinstance(piece, Bishop):
                enemyDict['bishop'].append(piece)
            elif isinstance(piece, Knight):
                enemyDict['knight'].append(piece)
            elif isinstance(piece, Pawn):
                enemyDict['pawn'].append(piece)

        tempQueen = Queen(self.side, self.x, self.y, self.gameinfo)
        tempRook = Rook(self.side, self.x, self.y, self.gameinfo)
        tempBishop = Bishop(self.side, self.x, self.y, self.gameinfo)
        tempKnight = Knight(self.side, self.x, self.y, self.gameinfo)
        tempPawn = Pawn(self.side, self.x, self.y, self.gameinfo)

        for piece, enemyPiece in zip([tempQueen, tempRook, tempBishop, tempKnight, tempPawn], enemyDict):
            for move in piece.getMoveset():
                if move.isOccupied(enemyDict[enemyPiece]) and (piece is not tempPawn or move.x != self.x):
                    self.attackers.append(enemyDict[enemyPiece])
                    check = True  
        return check
    

    def isInCheckmate(self):
        if not self.isInCheck() or len(self.getMoveset()) > 0: #The King has to have no moves and be in check
            return False
        
        if self.side == "WHITE":
            pieceList = self.gameinfo.whiteList
        else:
            pieceList = self.gameinfo.blackList

        tempQueen = Queen(self.side, self.x, self.y, self.gameinfo)
        tempRook = Rook(self.side, self.x, self.y, self.gameinfo)
        tempBishop = Bishop(self.side, self.x, self.y, self.gameinfo)
        tempKnight = Knight(self.side, self.x, self.y, self.gameinfo)
        tempPawn = Pawn(self.side, self.x, self.y, self.gameinfo)

        for attacker in self.attackers:
            for tempPiece in [tempQueen, tempRook, tempBishop, tempKnight, tempPawn]:
                if isinstance(attacker, type(tempPiece)):
                    intersecting = list(set(attacker.getMoveset()).intersection(tempPiece.getMoveset()))
                    intersecting.append(self.gameinfo.board[attacker.y][attacker.x])
                    for ally in pieceList:
                        if not isinstance(ally, King):
                            allyBlockPath = list(set(intersecting).intersection(ally.getMoveset()))
                            if len(allyBlockPath) > 0:
                                return False

        return True

    def __str__(self):
        return f'{self.side} King {self.gameinfo.board[self.y][self.x]}'

