"""
Name: Pylyp Lyamov
Date created: September 20, 2026
Course: COP2373 - Programming Exercise 2

Program description:
    This program checks an email message for signs of spam. The user types
    in the message, and the program scans it for 30 words and phrases that
    commonly appear in spam. Every occurrence of one of those words or
    phrases adds one point to the message's spam score. The program then
    rates how likely the message is to be spam based on that score, and
    displays the score, the rating, and the words and phrases that caused
    the score.
"""

import re


def get_spam_keywords():
    """
    Provides the list of 30 words and phrases that commonly appear in spam.

    Parameters:
        None

    Variables:
        keywords (list of str): The 30 spam words and phrases, all in lower case.

    Logic:
        1. Build the list of 30 words and phrases, written in lower case so
           that the scan can compare them without worrying about case.
        2. Return the list.

    Return:
        list of str: The 30 spam words and phrases.
    """
    # The list was compiled from published spam trigger word lists. It is
    # kept in one place so that changing a phrase never touches the scan.
    keywords = [
        "free", "winner", "congratulations", "you have been selected",
        "click here", "act now", "limited time", "urgent", "buy now",
        "order now", "no risk", "guaranteed", "no obligation", "cash bonus",
        "make money", "earn extra income", "work from home", "lose weight",
        "credit card", "lowest price", "no cost", "dear friend", "apply now",
        "million dollars", "prize", "double your", "this is not spam",
        "verify your account", "offer expires", "special promotion"
    ]

    return keywords


def get_email_message():
    """
    Asks the user to type in an email message, one line at a time, and
    returns the whole message as a single string.

    Parameters:
        None

    Variables:
        lines (list of str): Every line the user has typed so far.
        line (str): The most recent line typed by the user.
        message (str): All of the lines joined together with spaces.

    Logic:
        1. Explain to the user how to enter the message and how to finish.
        2. Loop, reading one line at a time.
        3. Stop reading when the user presses Enter on an empty line, but
           only if at least one line of text has been entered.
        4. Join the lines with spaces so that a phrase split across two
           lines can still be found.
        5. Return the message.

    Return:
        str: The complete email message entered by the user.
    """
    print("Enter your email message below. You may use as many lines as you like.")
    print("Press Enter on an empty line when you are finished.")
    print()

    lines = []

    # Keep reading until the user signals the end with an empty line.
    while True:
        line = input("> ")

        # An empty line means the user is done, unless nothing has been
        # entered yet, because an empty message cannot be scored.
        if line.strip() == "":
            if len(lines) == 0:
                print("Please enter at least one line of text.")
            else:
                break
        else:
            lines.append(line.strip())

    # Spaces between lines let phrases such as "click here" match even when
    # the user typed "click" at the end of one line and "here" on the next.
    message = " ".join(lines)

    return message


def scan_message(message, keywords):
    """
    Scans the message for every spam word or phrase and counts how many
    times each one appears.

    Parameters:
        message (str): The email message entered by the user.
        keywords (list of str): The spam words and phrases to look for.

    Variables:
        matches (list of tuple): Each found phrase paired with the number of
                                 times it appeared, for example ("free", 2).
        keyword (str): The spam word or phrase currently being searched for.
        pattern (str): A regular expression that matches the keyword only as
                       whole words, ignoring upper and lower case.
        count (int): How many times the current keyword appears in the message.

    Logic:
        1. Start with an empty list of matches.
        2. Loop through each keyword.
        3. Build a pattern that matches the keyword as whole words, so that
           "free" is found in "FREE gift!" but not inside "freedom".
        4. Count how many times the pattern appears in the message, ignoring case.
        5. If the keyword appeared at least once, add it and its count to
           the list of matches.
        6. Return the list of matches.

    Return:
        list of tuple: The spam words and phrases found, each with its count.
    """
    matches = []

    for keyword in keywords:
        # \b marks a word boundary, so the keyword has to stand on its own
        # rather than being buried inside a longer word such as "freedom".
        pattern = r"\b" + re.escape(keyword) + r"\b"

        # Count every occurrence, treating upper and lower case the same,
        # because "FREE" and "free" are the same word to a spam filter.
        count = len(re.findall(pattern, message, re.IGNORECASE))

        # Only keywords that actually appeared are worth reporting.
        if count > 0:
            matches.append((keyword, count))

    return matches


def rate_likelihood(spam_score):
    """
    Turns the spam score into a sentence describing how likely it is that
    the message is spam.

    Parameters:
        spam_score (int): The total number of spam words and phrases found.

    Variables:
        likelihood (str): The sentence chosen for this score.

    Logic:
        1. If the score is 0, the message is very unlikely to be spam.
        2. If the score is 1 or 2, the message is unlikely to be spam.
        3. If the score is 3, 4 or 5, the message is likely to be spam.
        4. If the score is 6 or more, the message is very likely to be spam.
        5. Return the chosen sentence.

    Return:
        str: A sentence describing the likelihood that the message is spam.
    """
    # The thresholds rise with the score: a single stray word is normal in
    # an honest email, but several together are the mark of spam.
    if spam_score == 0:
        likelihood = "This message is very unlikely to be spam."
    elif spam_score <= 2:
        likelihood = "This message is unlikely to be spam."
    elif spam_score <= 5:
        likelihood = "This message is likely to be spam."
    else:
        likelihood = "This message is very likely to be spam."

    return likelihood


def display_results(spam_score, likelihood, matches):
    """
    Displays the spam score, the likelihood rating, and the words and
    phrases that caused the score.

    Parameters:
        spam_score (int): The total number of spam words and phrases found.
        likelihood (str): The sentence describing how likely the message is spam.
        matches (list of tuple): Each spam word or phrase found, with its count.

    Variables:
        keyword (str): One spam word or phrase that was found.
        count (int): How many times that word or phrase appeared.
        times (str): The word "time" or "times", chosen to match the count.

    Logic:
        1. Display the spam score and the likelihood sentence.
        2. If nothing was found, say so and stop.
        3. Otherwise, loop through the matches and display each word or
           phrase with the number of times it appeared.

    Return:
        None
    """
    print()
    print(f"Spam score: {spam_score}")
    print(f"Spam likelihood: {likelihood}")
    print()

    # A clean message has nothing to list, so say that instead of showing
    # an empty heading.
    if len(matches) == 0:
        print("No spam words or phrases were found in the message.")
        return

    print("Words and phrases that raised the spam score:")

    for keyword, count in matches:
        # "1 times" would read poorly, so match the word to the count.
        if count == 1:
            times = "time"
        else:
            times = "times"

        print(f'  "{keyword}" - found {count} {times}')


def main():
    """
    Runs the spam checker from start to finish.

    Parameters:
        None

    Variables:
        keywords (list of str): The 30 spam words and phrases.
        message (str): The email message entered by the user.
        matches (list of tuple): The spam words and phrases found, with counts.
        spam_score (int): Accumulator that adds up the count of every match.
        keyword (str): One found spam word or phrase (used while accumulating).
        count (int): The number of times that word or phrase appeared.
        likelihood (str): The sentence describing how likely the message is spam.

    Logic:
        1. Get the list of spam keywords.
        2. Ask the user for the email message.
        3. Scan the message for the keywords.
        4. Add the count of every match to the spam score accumulator.
        5. Rate the likelihood that the message is spam.
        6. Display the results.

    Return:
        None
    """
    print("Email Spam Checker")
    print("=" * 18)
    print()

    keywords = get_spam_keywords()
    message = get_email_message()
    matches = scan_message(message, keywords)

    # Every occurrence of a spam word or phrase is worth one point, so the
    # score is simply the sum of all the counts.
    spam_score = 0
    for keyword, count in matches:
        spam_score += count

    likelihood = rate_likelihood(spam_score)
    display_results(spam_score, likelihood, matches)


# Program entry point
if __name__ == "__main__":
    main()
