"""
Name: Pylyp Lyamov
Date created: November 8, 2026
Course: COP2373 - Programming Exercise 7

Program description:
    This program defines a BankAcct class that models a simple savings
    account. The account stores the owner's name, the account number, the
    amount on deposit and the annual interest rate. It can take deposits
    and withdrawals, report its balance, adjust its interest rate, and
    calculate the interest earned over a given number of days. The __str__
    method displays the balance together with the interest the account
    would earn over thirty days and over a full year. The test function at
    the bottom of the file exercises every method, including the cases that
    should be refused, and reports whether each one behaved as expected.
"""


class BankAcct:
    """A simple savings account with a balance and an annual interest rate."""

    def __init__(self, name, account_number, amount=0.0, interest_rate=0.0):
        """
        Creates a new account.

        Parameters:
            name (str): The name of the account holder.
            account_number (str): The number identifying the account.
            amount (float): The amount the account starts with.
            interest_rate (float): The annual interest rate as a percentage,
                                   so 2.5 means 2.5 percent per year.

        Variables:
            None beyond the attributes being stored.

        Logic:
            1. Refuse a starting amount below zero, because an account
               cannot open already overdrawn.
            2. Refuse an interest rate below zero.
            3. Store the four pieces of state on the object.

        Return:
            None
        """
        # The two amounts are checked here so an invalid account can never
        # be created in the first place.
        if amount < 0:
            raise ValueError("The starting amount cannot be negative.")

        if interest_rate < 0:
            raise ValueError("The interest rate cannot be negative.")

        self.name = name
        self.account_number = account_number
        self.amount = round(float(amount), 2)
        self.interest_rate = float(interest_rate)

    def deposit(self, amount):
        """
        Adds money to the account.

        Parameters:
            amount (float): The amount to add.

        Variables:
            None beyond the balance being updated.

        Logic:
            1. Refuse an amount that is zero or negative, because that is a
               withdrawal and not a deposit.
            2. Add the amount to the balance, rounded to the nearest cent.
            3. Return the new balance.

        Return:
            float: The balance after the deposit.
        """
        if amount <= 0:
            raise ValueError("The deposit amount must be greater than zero.")

        # Rounding on every change keeps the balance at whole cents instead
        # of letting floating point error build up over many transactions.
        self.amount = round(self.amount + amount, 2)

        return self.amount

    def withdraw(self, amount):
        """
        Takes money out of the account.

        Parameters:
            amount (float): The amount to take out.

        Variables:
            None beyond the balance being updated.

        Logic:
            1. Refuse an amount that is zero or negative.
            2. Refuse an amount larger than the balance, because this
               account does not allow an overdraft.
            3. Subtract the amount from the balance.
            4. Return the new balance.

        Return:
            float: The balance after the withdrawal.
        """
        if amount <= 0:
            raise ValueError("The withdrawal amount must be greater than zero.")

        # The message names both figures so the account holder can see how
        # much is actually available.
        if amount > self.amount:
            raise ValueError(f"The withdrawal of ${amount:.2f} is more than "
                             f"the balance of ${self.amount:.2f}.")

        self.amount = round(self.amount - amount, 2)

        return self.amount

    def get_balance(self):
        """
        Reports the amount currently in the account.

        Parameters:
            None

        Variables:
            None

        Logic:
            1. Return the balance.

        Return:
            float: The amount currently on deposit.
        """
        return self.amount

    def set_interest_rate(self, interest_rate):
        """
        Changes the annual interest rate of the account.

        Parameters:
            interest_rate (float): The new annual rate as a percentage.

        Variables:
            None beyond the rate being replaced.

        Logic:
            1. Refuse a rate below zero.
            2. Store the new rate.
            3. Return the new rate.

        Return:
            float: The interest rate now in effect.
        """
        if interest_rate < 0:
            raise ValueError("The interest rate cannot be negative.")

        self.interest_rate = float(interest_rate)

        return self.interest_rate

    def calculate_interest(self, days):
        """
        Calculates the simple interest the balance earns over a number of days.

        Parameters:
            days (int): The number of days the money is on deposit.

        Variables:
            yearly_interest (float): The interest the balance would earn in
                                     one full year at the current rate.
            interest (float): The share of that yearly interest belonging to
                              the number of days given.

        Logic:
            1. Refuse a number of days that is zero or negative.
            2. Work out the interest for one full year by applying the rate,
               which is a percentage, to the balance.
            3. Take the share of that amount for the days requested, using a
               365 day year.
            4. Return the result rounded to the nearest cent.

        Return:
            float: The interest earned over the given number of days.
        """
        if days <= 0:
            raise ValueError("The number of days must be greater than zero.")

        # The rate is held as a percentage, so it is divided by 100 before
        # it is applied to the balance.
        yearly_interest = self.amount * (self.interest_rate / 100)

        # Simple interest: the year's interest shared out over the days the
        # money was actually on deposit.
        interest = yearly_interest * (days / 365)

        return round(interest, 2)

    def __str__(self):
        """
        Builds the text shown when the account is printed.

        Parameters:
            None

        Variables:
            thirty_days (float): The interest the balance earns in 30 days.
            one_year (float): The interest the balance earns in 365 days.
            lines (list of str): The lines of the finished description.

        Logic:
            1. Calculate the interest for 30 days and for one year, unless
               the balance is zero, in which case both are zero.
            2. Build one line each for the heading, the balance, the rate
               and the two interest amounts.
            3. Join the lines into a single string and return it.

        Return:
            str: A description of the account, its balance and its interest.
        """
        # calculate_interest refuses a zero day count, and an empty account
        # earns nothing anyway, so the zero case is handled directly.
        if self.amount == 0 or self.interest_rate == 0:
            thirty_days = 0.0
            one_year = 0.0
        else:
            thirty_days = self.calculate_interest(30)
            one_year = self.calculate_interest(365)

        lines = [
            f"Account {self.account_number} - {self.name}",
            f"  Balance: ${self.amount:.2f}",
            f"  Interest rate: {self.interest_rate:.2f}% per year",
            f"  Interest after 30 days: ${thirty_days:.2f}",
            f"  Interest after 365 days: ${one_year:.2f}",
        ]

        return "\n".join(lines)


def test_bank_acct():
    """
    Tests every method of the BankAcct class and reports the results.

    Parameters:
        None

    Variables:
        account (BankAcct): The account the tests are run against.
        results (list of tuple): Each check as its description and whether
                                 it produced the expected answer.
        passed (int): Accumulator counting the checks that passed.
        description (str): The description of the check being reported.
        was_correct (bool): Whether that check produced the expected answer.
        outcome (str): The word "PASS" or "FAIL" for the current check.
        error (ValueError): The refusal raised by a method that was given
                            an invalid value.

    Logic:
        1. Create an account and display it, which exercises __str__.
        2. Call each method with a valid value and record whether the
           answer matched the expected one.
        3. Call each method with an invalid value and record whether it was
           refused with a message.
        4. Display every check with PASS or FAIL, then the total.
        5. Display the account again so the final state can be seen.

    Return:
        None
    """
    print("BankAcct Class Test")
    print("=" * 19)
    print()

    # Creating the account also exercises __init__ and __str__.
    account = BankAcct("Pylyp Lyamov", "1001", 500.00, 2.50)
    print("The account as created:")
    print(account)
    print()

    results = []

    # Each check records what was tried and whether the result was right.
    results.append((f"deposit(250.00) gives a balance of ${account.deposit(250.00):.2f}",
                    account.get_balance() == 750.00))

    results.append((f"withdraw(100.50) gives a balance of ${account.withdraw(100.50):.2f}",
                    account.get_balance() == 649.50))

    results.append((f"get_balance() returns ${account.get_balance():.2f}",
                    account.get_balance() == 649.50))

    results.append((f"set_interest_rate(3.75) returns {account.set_interest_rate(3.75):.2f}%",
                    account.interest_rate == 3.75))

    # 649.50 at 3.75% for 30 days is 2.00, and for a full year is 24.36.
    results.append((f"calculate_interest(30) returns ${account.calculate_interest(30):.2f}",
                    account.calculate_interest(30) == 2.00))

    results.append((f"calculate_interest(365) returns ${account.calculate_interest(365):.2f}",
                    account.calculate_interest(365) == 24.36))

    # The remaining checks give each method a value it must refuse. The
    # test passes only when a ValueError is raised.
    try:
        account.deposit(-50.00)
        results.append(("deposit(-50.00) was wrongly allowed", False))
    except ValueError as error:
        results.append((f"deposit(-50.00) refused: {error}", True))

    try:
        account.withdraw(10000.00)
        results.append(("withdraw(10000.00) was wrongly allowed", False))
    except ValueError as error:
        results.append((f"withdraw(10000.00) refused: {error}", True))

    try:
        account.set_interest_rate(-1.00)
        results.append(("set_interest_rate(-1.00) was wrongly allowed", False))
    except ValueError as error:
        results.append((f"set_interest_rate(-1.00) refused: {error}", True))

    try:
        account.calculate_interest(0)
        results.append(("calculate_interest(0) was wrongly allowed", False))
    except ValueError as error:
        results.append((f"calculate_interest(0) refused: {error}", True))

    try:
        BankAcct("Test Account", "9999", -100.00)
        results.append(("BankAcct with a negative amount was wrongly allowed", False))
    except ValueError as error:
        results.append((f"BankAcct(amount=-100.00) refused: {error}", True))

    print("Testing the methods")
    print("=" * 76)

    # The accumulator starts at zero because no check has been reported yet.
    passed = 0

    for description, was_correct in results:
        if was_correct:
            outcome = "PASS"
            passed += 1
        else:
            outcome = "FAIL"

        print(f"{outcome}  {description}")

    print("=" * 76)
    print(f"{passed} of {len(results)} tests passed.")
    print()

    # Printing the account again shows the state left by the tests.
    print("The account after the tests:")
    print(account)


# Program entry point
if __name__ == "__main__":
    # Run every test against the BankAcct class.
    test_bank_acct()
