"""
Name: Pylyp Lyamov
Date created: August 30, 2026
Course: COP2373 - Programming Exercise 2

Program description:
    This program runs the pre-sale for a limited number of cinema tickets.
    Only 20 tickets exist for the showing, and no single buyer may purchase
    more than 4 of them. The program asks each buyer in turn how many
    tickets they want, reports how many tickets are still available after
    that purchase, and continues until every ticket has been sold. Once the
    pre-sale ends, the program reports how many buyers took part.
"""


def describe_count(count, singular, plural):
    """
    Joins a number to the singular or plural form of a word so that every
    message the program prints is grammatically correct.

    Parameters:
        count (int): The number of items being described.
        singular (str): The word to use when there is exactly one item.
        plural (str): The word to use for any other number of items.

    Variables:
        word (str): The form of the word chosen for this count.

    Logic:
        1. Choose the singular form when the count is exactly one.
        2. Otherwise choose the plural form.
        3. Join the count and the chosen word into one phrase.

    Return:
        str: A phrase such as "1 ticket" or "4 tickets".
    """
    # A count of one needs the singular word; every other count, including
    # zero, needs the plural.
    if count == 1:
        word = singular
    else:
        word = plural

    # Hand back the finished phrase so the caller can drop it into a sentence.
    return f"{count} {word}"


def get_ticket_request(tickets_remaining, max_per_buyer):
    """
    Asks the current buyer how many tickets they want and returns that
    number once it has passed every validation rule.

    Parameters:
        tickets_remaining (int): The number of tickets still available in the pre-sale.
        max_per_buyer (int): The largest number of tickets one buyer may purchase.

    Variables:
        purchase_limit (int): The most tickets this buyer may take, which is the
                              smaller of max_per_buyer and tickets_remaining.
        response (str): The raw text the buyer typed at the prompt.
        requested (int): The buyer's response converted to a whole number.

    Logic:
        1. Work out this buyer's purchase limit so that nobody can claim more
           tickets than the pre-sale still has.
        2. Loop until the buyer supplies a valid request.
        3. Prompt the buyer for the number of tickets they want.
        4. Reject the entry with a polite message if it is not a whole number.
        5. Reject the entry with a polite message if it is below 1 or above
           the purchase limit.
        6. Return the request as soon as it is valid.

    Return:
        int: The validated number of tickets this buyer is purchasing.
    """
    # A buyer may never take more than the per-buyer limit, and never more
    # than what is actually left, so the smaller of the two rules the sale.
    purchase_limit = min(max_per_buyer, tickets_remaining)

    # Keep asking until the buyer gives an answer the pre-sale can accept.
    while True:
        response = input(f"How many tickets would you like to purchase (1-{purchase_limit})? ")

        # A buyer can type anything at all, so confirm the entry is a whole
        # number before treating it as a ticket count.
        if not response.strip().isdigit():
            print("Please enter a whole number.")

        else:
            requested = int(response)

            # Enforce the two rules of the sale: at least one ticket per
            # buyer, and never more than this buyer's purchase limit.
            if requested < 1:
                print("Please purchase at least 1 ticket.")
            elif requested > purchase_limit:
                print("Sorry, you may only purchase up to "
                      + describe_count(purchase_limit, "ticket", "tickets") + ".")
            else:
                return requested


def run_ticket_presale(total_tickets=20, max_per_buyer=4):
    """
    Runs the ticket pre-sale from the first buyer until the last ticket is
    sold, reporting the number of tickets remaining after every purchase.

    Parameters:
        total_tickets (int): The number of tickets available in the pre-sale.
        max_per_buyer (int): The largest number of tickets one buyer may purchase.

    Variables:
        tickets_sold (int): Accumulator that adds up every ticket sold so far.
        buyer_count (int): Accumulator that counts how many buyers have purchased.
        tickets_remaining (int): The tickets still available at that point in the sale.
        requested (int): The number of tickets the current buyer purchased.

    Logic:
        1. Set both accumulators to zero and welcome the buyers.
        2. Loop while tickets are still available.
        3. Calculate the tickets remaining and announce whose turn it is.
        4. Call get_ticket_request to obtain a valid purchase.
        5. Add the purchase to the ticket accumulator and add one to the
           buyer accumulator.
        6. Display the number of tickets remaining after the purchase, and
           announce the sell-out when the last ticket is gone.
        7. Return the number of buyers once every ticket has been sold.

    Return:
        int: The total number of buyers who purchased tickets.
    """
    # Both accumulators start at zero because nothing has been sold yet.
    tickets_sold = 0
    buyer_count = 0

    # State the two rules of the pre-sale before the first buyer is served.
    print("Welcome to the cinema ticket pre-sale!")
    print(f"There are {total_tickets} tickets available, "
          f"and each buyer may purchase up to {max_per_buyer} tickets.")

    # The pre-sale continues until the accumulator shows every ticket is sold.
    while tickets_sold < total_tickets:
        # Recalculate what is left so the next buyer is offered a truthful limit.
        tickets_remaining = total_tickets - tickets_sold

        # Number the prompt so each buyer knows it is their turn.
        print(f"\nBuyer {buyer_count + 1}:")
        requested = get_ticket_request(tickets_remaining, max_per_buyer)

        # Record the sale in both accumulators, then refresh the count of
        # what is left so the buyer is told the truth about availability.
        tickets_sold += requested
        buyer_count += 1
        tickets_remaining = total_tickets - tickets_sold

        # Confirm the purchase and report the remaining tickets, which is
        # the figure the buyer needs after every single sale.
        print("Thank you for purchasing "
              + describe_count(requested, "ticket", "tickets")
              + f". Tickets remaining: {tickets_remaining}.")

        # Only the final buyer should see the closing announcement.
        if tickets_remaining == 0:
            print("The pre-sale is now sold out!")

    # Hand the buyer count back so the caller can report the final total.
    return buyer_count


def display_buyer_total(buyer_count):
    """
    Displays the final result of the pre-sale to the user.

    Parameters:
        buyer_count (int): The total number of buyers who purchased tickets.

    Variables:
        buyer_phrase (str): The buyer count joined to the correct form of
                            the word "buyer".

    Logic:
        1. Build a correctly worded phrase for the number of buyers.
        2. Display the total number of buyers who took part in the pre-sale.

    Return:
        None
    """
    # Reuse the wording helper so the closing sentence reads correctly
    # whether one buyer or many took part.
    buyer_phrase = describe_count(buyer_count, "buyer", "buyers")

    # Report the final total that the pre-sale was asked to produce.
    print(f"\nAll of the tickets have been sold to a total of {buyer_phrase}.")


# Program entry point
if __name__ == "__main__":
    # Run the pre-sale and keep the number of buyers it reports.
    total_buyers = run_ticket_presale()

    # Display the final buyer total now that the pre-sale has ended.
    display_buyer_total(total_buyers)
