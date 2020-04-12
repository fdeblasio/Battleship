from random import randint
from colorama import Fore, Back, Style, init

init(autoreset=True)

size = 10
global gameOver
gameOver = False

A = ord('A')
OMEGA = ord('A') + size
preAlpha = A - 1

blank = Back.BLUE + " " + Style.RESET_ALL
hit = Back.RED + " " + Style.RESET_ALL
miss = Back.WHITE + " " + Style.RESET_ALL
sunk = Back.BLACK + " " + Style.RESET_ALL
ship = Back.CYAN + " " + Style.RESET_ALL

#gets a random value from a list
def randList(list):
    return list[randint(0, len(list) - 1)]

class Boat:
    #Destroyer/Patrol Boat 2
    #Submarine 3
    #Cruiser/Destroyer 3
    #Battleship 4
    #Carrier 5
    def __init__(self, length):
        self.length = length
        self.spaces = []
        self.strikes = []

class Board:
    #add variable for player or not. if player, can see boats (add boat color white/gray)
    def __init__(self):
        self.board = [['  '] + [' '*(1-x/(size-1)) + str(x+1) for x in range(size)]]
        for i in range(A, OMEGA):
            self.board.append([chr(i)] + [blank]*size)

        self.choices = [chr(x) + str(y) for x in range(A, OMEGA) for y in range(1, size + 1)]

        battleship = Boat(4)
        self.boats = {battleship}
        self.sunkBoats = set()
        for boat in self.boats:
            column = randint(A, OMEGA-1)
            row = randint(1, size + 1 - boat.length)
            for i in range(row, row + boat.length):
                self.board[column-preAlpha][i] = ship
                boat.spaces.append((chr(column), i))

    def toString(self):
        print "|-" + "-+"*len(self.board[0])
        for column in range(len(self.board)):
            rowPrint = "|"
            for row in range(len(self.board[0])):
                rowPrint += self.board[row][column] + "|"
            print rowPrint
            rowLines = "|-"
            for space in range(len(self.board[0])):
                rowLines += "-" + "+"
            print rowLines
        print

def attack(board, selection):
    global gameOver

    if selection not in board.choices:
        space = randList(board.choices)
        print selection, "is not a viable option. Using", space, "instead."
    else:
        space = selection
    print space
    letter = space[0]
    number = int(space[1:])
    column = ord(letter)-preAlpha
    row = number
    board.choices.remove(space)
    if board.board[column][row] == ship:
        for boat in board.boats:
            if (letter, number) in boat.spaces:
                boat.strikes.append(boat.spaces.pop(boat.spaces.index((letter, number))))
                if len(boat.strikes) == boat.length:
                    print "Sunk!"
                    for strike in boat.strikes:
                        sunkLetter = strike[0]
                        sunkNumber = int(strike[1])
                        board.board[ord(sunkLetter)-preAlpha][sunkNumber] = sunk
                    board.sunkBoats.add(boat)
                    if len(board.sunkBoats) == len(board.boats):
                        gameOver = True
                        break
                else:
                    print "Hit!"
                    board.board[column][row] = hit
    else:
        print "Miss"
        board.board[column][row] = miss
    board.toString()

#playerBoard = Board()
enemyBoard = Board()

'''enemyBoard.toString()
playerBoard.toString()'''

enemyBoard.toString()
turns = 0
while not gameOver:
    try:
        turns += 1
        target = raw_input("Turn " + str(turns) + ": Which space would you like to attack? ").upper().strip()
        attack(enemyBoard, target)
    except KeyboardInterrupt:
        print
        quit()

print "You took", turns, "turns out of a possible", str(size*size) + "."
print "Game Over!"
