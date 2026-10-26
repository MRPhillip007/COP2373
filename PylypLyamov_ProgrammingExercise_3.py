"""
Name: Pylyp Lyamov
Date created: September 26, 2026
Course: COP2373 - Programming Exercise 3

Program description:
    This program analyzes a user's monthly expenses. The user enters the
    expenses one at a time, giving the type of each expense, such as Rent
    or Groceries, and the amount spent on it. When the list is complete,
    the program uses the reduce function to calculate the total of all the
    expenses and to find the highest and the lowest expense. It then
    displays the total, followed by the highest and lowest expenses, each
    labeled with its type.
"""

from functools import reduce


def get_expenses():
    """
    Asks the user for their monthly expenses, one at a time, and returns the
    type and amount of every expense entered.

    Parameters:
        None

    Variables:
        expenses (list of tuple): The expenses entered so far, each stored as a
                                  (type, amount) pair, for example ("Rent", 1150.0).
        expense_number (int): The number of the expense being asked for next.
        prompt (str): The question used to ask for the type of expense.
        expense_type (str): The type of expense the user typed, such as "Rent".
        amount (float): The amount the user spends each month on that expense.

    Logic:
        1. Explain to the user how to enter their expenses.
        2. Start with an empty list of expenses.
        3. Loop, asking for the type of one expense at a time. From the second
           expense on, the prompt tells the user that pressing Enter without
           typing anything finishes the list.
        4. If the user presses Enter without typing a type, stop asking, but
           only if at least one expense has been entered.
        5. Otherwise, call get_expense_amount to ask for the amount, and add
           the (type, amount) pair to the list.
        6. Return the list of expenses.

    Return:
        list of tuple: Every expense entered, as (type, amount) pairs.
    """
    print("Enter your monthly expenses one at a time. For each expense, enter")
    print("its type, such as Rent or Groceries, and then the amount.")

    expenses = []

    # Keep asking for expenses until the user says the list is complete.
    while True:
        expense_number = len(expenses) + 1

        # At least one expense is needed for the analysis, so the way to
        # finish is only offered once the first expense has been entered.
        if expense_number == 1:
            prompt = "Type of expense 1: "
        else:
            prompt = f"Type of expense {expense_number} (or press Enter to finish): "

        # A blank line between expenses keeps each type next to its amount.
        print()
        expense_type = input(prompt).strip()

        # An empty type means the user is finished, unless nothing has been
        # entered yet, because there is nothing to analyze without an expense.
        if expense_type == "":
            if len(expenses) == 0:
                print("Please enter at least one expense.")
            else:
                break
        else:
            amount = get_expense_amount(expense_type)

            # Store the type and amount together so that the highest and
            # lowest expenses can be labeled with their types later.
            expenses.append((expense_type, amount))

    return expenses


def get_expense_amount(expense_type):
    """
    Asks the user how much they spend each month on one type of expense, and
    returns the amount once it is a valid amount of money.

    Parameters:
        expense_type (str): The type of expense the amount is for, such as "Rent".

    Variables:
        response (str): The raw text the user typed at the prompt.
        cleaned (str): The response with dollar signs, commas and surrounding
                       spaces removed.
        amount (float): The cleaned response as a number, rounded to the cent.

    Logic:
        1. Loop until the user enters a valid amount.
        2. Prompt the user for the amount spent on this type of expense.
        3. Remove any dollar signs, commas and surrounding spaces, so that an
           entry such as "$1,150" is read as 1150.
        4. Check that what is left is made of digits with at most one decimal
           point. This rejects words and negative numbers.
        5. Convert the entry to a number rounded to the nearest cent, and
           check that it is greater than zero.
        6. Return the amount as soon as it passes both checks. Otherwise,
           display a polite message and ask again.

    Return:
        float: The amount spent each month on this type of expense, in dollars.
    """
    # Keep asking until the user types an amount the program can use.
    while True:
        response = input(f"Amount spent on {expense_type}: $")

        # People often type money with a dollar sign or commas, as in $1,150,
        # so remove those characters and any spaces around the entry.
        cleaned = response.replace("$", "").replace(",", "").strip()

        # An amount of money is digits with at most one decimal point, so once
        # one point is removed, only digits should be left. This also rejects
        # words and negative numbers.
        if cleaned.replace(".", "", 1).isdecimal():
            # Money is counted in whole cents, so round to two decimal places.
            amount = round(float(cleaned), 2)

            # An expense has to cost something, so zero is not accepted.
            if amount > 0:
                return amount

        # The entry failed one of the checks, so show what is expected.
        print("Please enter an amount greater than zero, such as 1150 or 59.99.")


def analyze_expenses(expenses):
    """
    Uses the reduce function to calculate the total of all the expenses and to
    find the highest and the lowest expense.

    Parameters:
        expenses (list of tuple): Every expense entered, as (type, amount) pairs.

    Variables:
        total (float): The sum of the amounts of all the expenses.
        highest (tuple of (str, float)): The expense with the largest amount.
        lowest (tuple of (str, float)): The expense with the smallest amount.
        running_total (float): Lambda parameter: the total of the amounts
                               added so far.
        kept (tuple of (str, float)): Lambda parameter: the expense that has
                                      won every comparison so far.
        expense (tuple of (str, float)): Lambda parameter: the next expense
                                         from the list.

    Logic:
        1. Call reduce with a lambda that adds the amount of each expense to a
           running total. The total starts at 0, so after the last expense it
           holds the sum of every amount.
        2. Call reduce with a lambda that compares the expense kept so far with
           the next expense and keeps the one with the larger amount. The
           expense still kept after the last comparison is the highest.
        3. Call reduce with a lambda that keeps the expense with the smaller
           amount instead. The expense kept at the end is the lowest.
        4. Return the total, the highest expense and the lowest expense.

    Return:
        tuple: The total (float), then the highest expense and the lowest
               expense (each a tuple of (str, float)).
    """
    # reduce passes the running total and the next expense to the lambda,
    # which adds that expense's amount (item 1 of the pair) to the total. The
    # total starts at 0 because the list holds (type, amount) pairs, not numbers.
    total = reduce(lambda running_total, expense: running_total + expense[1],
                   expenses, 0)

    # With no starting value, reduce keeps the first expense and compares it
    # with each next expense in turn. The lambda keeps whichever amount is
    # larger, so the expense left at the end is the highest. When two amounts
    # are equal, the expense entered first is kept.
    highest = reduce(lambda kept, expense: expense if expense[1] > kept[1] else kept,
                     expenses)

    # The same comparison with < instead of > keeps the smaller amount each
    # time, so the expense left at the end is the lowest.
    lowest = reduce(lambda kept, expense: expense if expense[1] < kept[1] else kept,
                    expenses)

    return total, highest, lowest


def display_summary(total, highest, lowest):
    """
    Displays the total of the monthly expenses, followed by the highest and the
    lowest expense, each labeled with its type.

    Parameters:
        total (float): The sum of all the expense amounts.
        highest (tuple of (str, float)): The type and amount of the highest expense.
        lowest (tuple of (str, float)): The type and amount of the lowest expense.

    Variables:
        highest_type (str): The type of the highest expense, such as "Rent".
        highest_amount (float): The amount of the highest expense.
        lowest_type (str): The type of the lowest expense.
        lowest_amount (float): The amount of the lowest expense.

    Logic:
        1. Unpack the highest and lowest expenses into their types and amounts.
        2. Display a heading for the summary.
        3. Display the total expense in dollars and cents.
        4. Display the highest and the lowest expense, each labeled with its type.

    Return:
        None
    """
    # Split each (type, amount) pair so that the type can serve as the label.
    highest_type, highest_amount = highest
    lowest_type, lowest_amount = lowest

    print()
    print("Monthly Expense Summary")
    print("=" * 23)

    # ",.2f" shows an amount with commas between thousands and exactly two
    # decimal places, so 1150 is displayed as 1,150.00.
    print(f"Total expense:    ${total:,.2f}")
    print(f"Highest expense:  {highest_type} (${highest_amount:,.2f})")
    print(f"Lowest expense:   {lowest_type} (${lowest_amount:,.2f})")


def main():
    """
    Runs the monthly expense analyzer from start to finish.

    Parameters:
        None

    Variables:
        expenses (list of tuple): Every expense the user entered, as (type, amount) pairs.
        total (float): The sum of all the expense amounts.
        highest (tuple of (str, float)): The type and amount of the highest expense.
        lowest (tuple of (str, float)): The type and amount of the lowest expense.

    Logic:
        1. Display the title of the program.
        2. Ask the user for their monthly expenses.
        3. Analyze the expenses to find the total, the highest expense and the
           lowest expense.
        4. Display the results.

    Return:
        None
    """
    # Show the title of the program before asking for anything.
    print("Monthly Expense Analyzer")
    print("=" * 24)
    print()

    # Collect the expenses, analyze them with reduce, then show the results.
    expenses = get_expenses()
    total, highest, lowest = analyze_expenses(expenses)
    display_summary(total, highest, lowest)


# Program entry point
if __name__ == "__main__":
    main()
