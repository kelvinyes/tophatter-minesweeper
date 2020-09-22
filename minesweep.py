import random
import sys
import time

def print_mines_layout():
    global visible_values
    st = "   "
    for i in range(10):
        st += "     " + str(i)
    st += "\n"
 
    for r in range(10):
        st += "     "
        if r == 0:
            st += "_|_____|_____|_____|_____|_____|_____|_____|_____|_____|____|"
 
        st += "\n      "
        for col in range(10):
            if (col == 9):
                st += "|    "
            else:
                st += "|     "
        st += "|"
         
        st += "\n  " + str(r) + "   "
        for col in range(10):
            if (col == 9):
                st += "|  " + str(visible_values[r][col]) + " "
            else:
                st = st + "|  " + str(visible_values[r][col]) + "  "
        st += "|"
 
        st += "\n     "
        for col in range(10):
            st = st + "_|____"
        st += "|"
    print(st)
    print()

def setup():
    global all_values
    global visible_values

    for i in range(10):
        done = True
        while (done):
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (all_values[row][col] != "M"):
                done = False
                all_values[row][col] = "M"

    lateral = [-1, 1, 0, 0, -1, -1, 1, 1]
    vertical = [0, 0, -1, 1, -1, 1, -1, 1]

    for row in range(10):
        for col in range(10):
            if all_values[row][col] != "M":
                for i in range(8):
                    new_row = row + lateral[i]
                    new_col = col + vertical[i]
                    if new_row >= 0 and new_row < 10 and new_col >= 0 and new_col < 10 and all_values[new_row][new_col] == "M":
                        all_values[row][col] += 1

def reveal_zeros(row, col, coordinates):
    global visible_values
    global all_values
    global checked_squares

    lateral = [-1, 1, 0, 0, -1, -1, 1, 1]
    vertical = [0, 0, -1, 1, -1, 1, -1, 1]
    coordinate = (row, col)

    if coordinate not in checked_squares:
        checked_squares.append(coordinate)
        if (all_values[row][col] == 0):
            visible_values[row][col] = 0
            for i in range(8):
                new_row = row + lateral[i]
                new_col = col + vertical[i]
                if new_row >= 0 and new_row < 10 and new_col >= 0 and new_col < 10:
                    reveal_zeros(new_row, new_col, [])
        elif (all_values[row][col] != "M" and all_values[row][col] > 0):
            visible_values[row][col] = all_values[row][col]            

def check_win():
    global visible_values
    i = 0

    for row in range(10):
        for col in range(10):
            if (visible_values[row][col] != "X"):
                i += 1

    return i == 90

#This function attempts to solve a minesweeper game. It returns 0 when it fails and 1 when it succeeds.
def solve():
    global visible_values
    global all_values

    #First move is random.
    row = random.randint(0, 9)
    col = random.randint(0, 9)

    while (pick(row, col)):
        row, col = optimal_select()
        if (check_win()):
            return True
    
    return False

#Returns if the square has not been selected and if there are surrounding squares that reveal information.
def is_possible_selection(row, col):
    global visible_values

    if (visible_values[row][col] != "X"):
        return False

    lateral = [-1, 1, 0, 0, -1, -1, 1, 1]
    vertical = [0, 0, -1, 1, -1, 1, -1, 1]

    for x in range(8):
        new_row = row + lateral[x]
        new_col = row + vertical[x]
        if new_row >= 0 and new_row < 10 and new_col >= 0 and new_col < 10 and visible_values[new_row][new_col] != "X":
            return True

    return False

#This function selects the square with the highest percentage to be safe.
def optimal_select():
    global visible_values
    global all_values

    min_chance = 100
    row, col = 0, 0

    possible_squares = get_possible_squares()

    for coordinate in possible_squares:
        x = coordinate[0]
        y = coordinate[1]
        curr_chance = get_percentage(x, y, possible_squares)
        if (curr_chance < min_chance):
            min_chance = curr_chance
            row = x
            col = y

    return row, col

def get_percentage(row, col, possible_squares):
    global visible_values
    global confirmed_mines

    lateral = [-1, 1, 0, 0, -1, -1, 1, 1]
    vertical = [0, 0, -1, 1, -1, 1, -1, 1]

    percentages = []

    for j in range(8):
        new_row = row + lateral[j]
        new_col = col + vertical[j]
        if new_row >= 0 and new_row < 10 and new_col >= 0 and new_col < 10 and visible_values[new_row][new_col] != "X":
            num_bombs = visible_values[new_row][new_col]
            num_squares = 0
            for i in range(8):
                new_row2 = new_row + lateral[i]
                new_col2 = new_col + vertical[i]
                if new_row2 >= 0 and new_row2 < 10 and new_col2 >= 0 and new_col2 < 10 and visible_values[new_row2][new_col2] == "X":
                    num_squares += 1
            percentages.append(num_bombs / num_squares)

    if (len(percentages) == 0):
        return (10 - len(confirmed_mines)) / len(possible_squares)
    elif (percentages.count(1) != 0):
        confirmed_mines.append((row, col))
        return 1
    else:
        return sum(percentages) / len(percentages)

def get_possible_squares():
    global visible_values
    global confirmed_mines
    global checked_squares

    lst = []

    for x in range(10):
        for y in range(10):
            if (visible_values[x][y] == "X" and not ((x, y) in confirmed_mines) and not ((x, y) in checked_squares)):
                lst.append((x, y))
    
    return lst

def pick(row, col):
    global visible_values
    global all_values

    #Signifies we picked a mine.
    if (all_values[row][col] == "M"):
        return False

    if (all_values[row][col] == 0):
        reveal_zeros(row, col, [])

    checked_squares.append((row, col))

    visible_values[row][col] = all_values[row][col]
    return True

if __name__ == "__main__":

    if (len(sys.argv) != 2 or (sys.argv[1] != "play" and sys.argv[1] != "solve")):
        print("Incorrect program arguments. Either type \"python3 minesweep.py play\" or \"python3 minesweep.py solve\".")

    all_values = [[0 for i in range(10)] for x in range(10)]
    visible_values = [["X" for i in range(10)] for x in range(10)] 
    confirmed_mines = []
    checked_squares = []

    setup()
    
    #Running a solver for the game.
    if (sys.argv[1] == "solve"):
        t0 = time.process_time()
        print("Attempting to solve 100,000 puzzles.")
        num_solved = 0
        for i in range(1, 100001):
            if (solve()):
                num_solved += 1
            print("Currently solved " + str(num_solved / (i)) + "% of " + str(i) + " puzzles.", end='\r')
            all_values = [[0 for i in range(10)] for x in range(10)]
            visible_values = [["X" for i in range(10)] for x in range(10)] 
            confirmed_mines = []
            checked_squares = []
            setup()
        t1 = time.process_time() - t0
        print()
        print()
        print("Successfully solved " + str(num_solved) + " out of 100,000 puzzles. Time elapsed: " + str(t1) + " seconds.")
        
    #Playing the game itself.
    if (sys.argv[1] == "play"):
        print("")
        print("  Welcome to Minesweeper!")
        print("  X on the board represents an unchecked area.")
        print("  A number on the board represents how many bombs are surrounding that square.")

        game_ongoing = True

        while game_ongoing:
            print_mines_layout()
            try:
                user_input = list(map(int, input("Enter row number followed by a space and column number (ex.\"4 3\") of a square that is marked with an \"X\":").split()))
            except ValueError:
                print("")
                print("Make sure you're entering two numbers separated by a space! (ex.\"1 2\")")
                continue

            if (len(user_input) != 2):
                print("")
                print("Enter only two numbers separated by a space!")
                continue

            row = user_input[0]
            col = user_input[1]

            if (visible_values[row][col] != "X"):
                print("")
                print("This square has already been revealed! Pick another pair.")

            elif (all_values[row][col] == "M"):
                visible_values = all_values
                print_mines_layout()
                game_ongoing = False
                print("")
                print("Game over! You stepped on a mine.")

            elif (all_values[row][col] == 0):
                coordinates = []
                reveal_zeros(row, col, coordinates)

            elif (all_values[row][col] > 0):
                visible_values[row][col] = all_values[row][col]

            if (check_win()):
                visible_values = all_values
                print_mines_layout()
                game_ongoing = False
                print("")
                print("Congratulations! You win!")