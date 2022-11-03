# This code will gather inputs (deposit amount, number of lines to bet on & bet amount on each line). 
# The game will randomise the items within the slot (symbols A-D) for each bet placed and calculate the winnings and updated balance based on the result




import random

# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "A": 3,
    "B": 4,
    "C": 5,
    "D": 6
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

# Function to check if the user won or lost
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    # Loop through every row
    for line in range(lines):
        # Check the symbol in the first column of the row
        symbol = columns[0][line]
        # Loop through every column and check for that symbol in every next column/row
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        # If a line is a match, calculate winnings for that line by multiplying symbol value x bet
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    return winnings, winning_lines


def slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    # Loop through dict, add each symbol and symbol count to all_symbols list (ex: A 3x)
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    # Define columns list
    columns = []
    # Generate a seperate column for however many columns we have (ex: do it 3x)
    for _ in range(cols):
        column = []
        # current symbols is what we can currently select. Copy of all_symbols
        current_symbols = all_symbols[:]
        # Loop through however many values we need in each row and select a random value from copied list
        for _ in range(rows):
            value = random.choice(current_symbols)
            # Remove value from selectable (copied) list and update the column list
            current_symbols.remove(value)
            column.append(value)
        # Add column to columns list
        columns.append(column)

    return columns

# Function to print the slot machine & transpose the items from the row to a column

def print_slot_machine(columns):
    # Loop through every row, for every row, we loop through every column
    for row in range(len(columns[0])):
        # For every column, we only print current row we're on. i & Enumerate checks the index we're on
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()

    # Function for the user to input their deposit

def deposit():
    # Loop until the condition is met, checking if the input is a digit and meets the minimum deposit amount
    while True:
        amount = input("Please enter your deposit amount £")
        if amount.isdigit():
            # Convert input in to integer, as the input is currently a string
            amount = int(amount)
        if amount >= 5:
            break
        else:
            print("The minimum deposit value is £5.")

    return amount

# Function for user to select the amount of lines they would like to bet on

def get_number_of_lines():
    while True:
        # String concatenation in case MAX_LINES changes in the future. Returns (1-3)?
        lines = input("Please enter the number of lines you want to bet on (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            # Check if input is between the parameters
        if 1 <= lines <= MAX_LINES:
            break
        else:
            print("Enter a valid number of lines")

    return lines

# Ask how much money they would like to bet on each line

def get_bet():
    while True:
        amount = input("What would you like to bet on each line? £")
        if amount.isdigit():
            amount = int(amount)
            # Check if bet amount is between the parameters for each line. Specified at the top
        if MIN_BET <= amount <= MAX_BET:
            break
        else:
            print(f"The bet amount must be between £{MIN_BET} - £{MAX_BET}.")

    return amount

# Main function that stores all user inputs, checks if the balance >= total bet and runs the game
def spin(balance):
    # Change get_number_of_lines input to 'lines'
    lines = get_number_of_lines()
    # While loop to check the balance >= total bet. If not, ask the user if they want to deposit more money.
    while True:
        # Change get_bet input to 'bet'
        bet = get_bet()
        # Calculate total bet
        total_bet = bet * lines

        if total_bet > balance:
            print(
                f"You do not have sufficient funds. Your current balance is £{balance} ")

            # Ask the user if they want to deposit more money to their balance
            more_money = input("Do you want to deposit more money? (Y/N) ")

            # Ask the user how much they want to deposit and add that to their balance. Ask their bet input again
            if more_money == "Y":
                newbalance = input("How much would you like to deposit? £")
                if newbalance.isdigit():
                    newbalance = int(newbalance)
                    if newbalance >= 5:
                        balance = balance + newbalance
                        print(f"Your new balance is {balance}")
                        newlines = get_number_of_lines()
                        newbet = get_bet()
                        total_bet = newbet * newlines
                        print(f"You are betting £{newbet} on {newlines} lines. Total bet is £{total_bet}")
                break

            # If no, ask if they'd like to make another bet with their balance. If not, end game
            elif more_money == "N":
                play_again = input("Would you like to make another bet? (Y/N) ")
                if play_again == "Y":
                    newlines = get_number_of_lines()
                    newbet = get_bet()
                    total_bet = newbet * newlines
                    print(f"You are betting £{newbet} on {newlines} lines. Total bet is £{total_bet}")
                    break
                if play_again == "N":
                    print("Thank you for playing")
                    exit()
        elif total_bet<= balance:
            print(f"You are betting £{bet} on {lines} lines. Total bet is £{total_bet}")
        break

    slots = slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)

    if winnings == 0:
        balance = (balance - total_bet) + winnings

    if winnings != 0:
        balance = (balance - total_bet) + winnings

    print(f"You won £{winnings}.")
    print(f"You won on lines:", *winning_lines)
    print(f"Current balance is £{balance}")
    return balance

# Main function that starts the game
def main():
    balance = deposit()
    while True:
        if balance == 0:
            more_money = input("Do you want to deposit more money? (Y/N) ")
            if more_money == "Y":
                newbalance = input("How much would you like to deposit? £")
                if newbalance.isdigit():
                    newbalance = int(newbalance)
                    if newbalance >= 5:
                        balance = balance + newbalance
                        print(f"Your new balance is £{balance}")
                    else:
                        print("The minimum deposit value is £5")
                        more_money = input("Do you want to deposit more money? (Y/N) ")
                        if more_money.isalpha:
                            newbalance = input("How much would you like to deposit? £")
                            if newbalance.isdigit():
                                newbalance = int(newbalance)
                                if newbalance >= 5:
                                    balance = balance + newbalance
                                    print(f"Your new balance is £{balance}")
                        elif more_money == "N":
                            print("Thank you for playing")
                            break
            if more_money == "N":
                print("Thank you for playing")
                exit()

        answer = input("Press enter to play (q to quit).")
        if spin == "q":
            break
        balance = spin(balance)

main()
