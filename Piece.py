from abc import ABC, abstractmethod

class gameInfo:
    @classmethod
    def setGame(cls, board, whiteList, blackList, graveyard):
        cls.board = board
        cls.whiteList = whiteList
        cls.blackList = blackList
        cls.graveyard = graveyard

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
    def getMoveset(self): #TODO make sure all pieces have boundary checking
        pass
        

    def movesetFromList(self, posiions):
        moveset = []
        for i in posiions:
            if any(i in row for row in self.gameinfo.board):
                nextPiece = i.isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList)
                if nextPiece:
                    if nextPiece.side == self.side:
                        continue
                moveset.append(i)

        return moveset


        

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
        if self.side == "WHITE":
            yOffset = 1
            pieceList = self.gameinfo.blackList
        else:
            yOffset = -1
            pieceList = self.gameinfo.whiteList


        if not self.gameinfo.board[self.y + yOffset][self.x].isOccupied(self.gameinfo.blackList + self.gameinfo.whiteList):
            moveset.append(self.gameinfo.board[self.y + yOffset][self.x])

        if self.firstMove:
            moveset.append(self.gameinfo.board[self.y + yOffset * 2][self.x])

        killLeft = self.gameinfo.board[self.y + yOffset][self.x - 1].isOccupied(pieceList)
        killRight = self.gameinfo.board[self.y + yOffset][self.x + 1].isOccupied(pieceList)

        if killLeft:
            moveset.append(self.gameinfo.board[self.y + yOffset][self.x - 1])
        if killRight:
            moveset.append(self.gameinfo.board[self.y + yOffset][self.x + 1])
        #TODO add en passant
        return moveset
    
    
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
        #TODO add logic and call this method from king move
        pass
            

class Bishop(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)

    def move(self, option):
        return super().move(option)
    
    def getMoveset(self):
        moveset = []
        nextPiece = {}
        isBlocked = {'topLeft': False, 'topRight': False, 'bottomleft': False, 'bottomRight': False}

        for i in range(1, 8):
            for pieceName, offset in zip(isBlocked, [(i, -i),(i, i),(-i, -i),(-i, i)]):

                if self.y + offset[0] < 0 or self.y + offset[0] > 7 or self.x + offset[1] < 0 or self.x + offset[1] > 7:
                    continue

                if not isBlocked[pieceName]:
                    nextPiece[pieceName] = self.gameinfo.board[self.y + offset[0]][self.x + offset[1]].isOccupied(self.gameinfo.board.blackList + self.gameinfo.board.whiteList)
                else: 
                    nextPiece[pieceName] = None

                if nextPiece[pieceName]:
                    isBlocked[pieceName] = True
                    if nextPiece[pieceName].side != self.side:
                        moveset.append(Position(nextPiece[pieceName].x, nextPiece[pieceName].y))
                else:
                    moveset.append(Position(self.x + offset[1], self.y + offset[0]))

        return moveset
    
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
        moveset = super.movesetFromList(movements)
        return moveset


class King(Piece):

    def __init__(self, side, x, y, gameinfo):
        super().__init__(side, x, y, gameinfo)
        self.firstMove = True

    def move(self, option):
        #TODO check if move was a castle then call the rooks castle function

        super().move(option)

        self.firstMove = False

    def getMoveset(self):
        movements = []
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                if xOffset == 0 and yOffset == 0:
                    continue
                movements.append(Position(self.x + xOffset, self.y + yOffset))
        moveset = super.movesetFromList(movements)

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

            if leftRook.firstMove and leftClear:
                moveset.append(currentRow[2])
            elif rightRook.firstMove and rightClear:
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
                    check = True  
        return check

        
    
    #TODO for checkmakes we can check for a isInCheck and then check to see if length of moveset is 0  and then check if anything can block it (we only need to check bishops and rook paths from king position)

