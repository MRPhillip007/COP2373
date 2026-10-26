"""
Name: Pylyp Lyamov
Date created: October 25, 2026
Course: COP2373 - Programming Exercise 5

Program description:
    This program breaks a paragraph into its individual sentences. The user
    types a paragraph, which may contain sentences that begin with numbers,
    such as "1. The rent went up." The program uses a regular expression to
    split the paragraph wherever one sentence ends and the next begins, then
    displays each sentence on its own line and reports how many sentences the
    paragraph contained. After that it runs a set of built-in tests that show
    the splitting is correct on known paragraphs.
"""

import re


def split_into_sentences(paragraph):
    """
    Splits a paragraph into a list of its individual sentences.

    Parameters:
        paragraph (str): The paragraph entered by the user.

    Variables:
        pattern (str): The regular expression that describes the gap between
                       the end of one sentence and the start of the next.
        pieces (list of str): The parts returned by the split, before the
                              blank ones are removed.
        sentences (list of str): The finished sentences, trimmed of spaces.

    Logic:
        1. Build a pattern that splits on the whitespace following a period,
           an exclamation point or a question mark, allowing a closing quote
           or bracket to stay with the sentence it ends.
        2. Refuse to split after a number that begins a sentence, such as the
           "1." in "1. The rent went up", because that period does not end a
           sentence.
        3. Refuse to split after a common abbreviation such as Mr. or Dr.
        4. Split the paragraph on that pattern.
        5. Remove the spaces around each piece and drop any empty pieces.
        6. Return the list of sentences.

    Return:
        list of str: Each sentence found in the paragraph, in order.
    """
    # A decimal number such as 3.50 needs no special rule: its period is not
    # followed by a space, so the pattern below never splits there.
    pattern = (
        # Split just after an ending mark, or after a closing quote or
        # bracket that follows one, so the quote stays with its sentence.
        r"(?:(?<=[.!?])|(?<=[.!?][\"')\]]))"

        # A short number at the start of a sentence is a label, not an
        # ending, so do not split after "1." or "10." at the beginning of
        # the paragraph or straight after a space.
        r"(?<!^\d\.)(?<!^\d\d\.)"
        r"(?<!\s\d\.)(?<!\s\d\d\.)"

        # These abbreviations end in a period without ending a sentence.
        r"(?<!\bMr\.)(?<!\bMs\.)(?<!\bDr\.)(?<!\bSt\.)"
        r"(?<!\bJr\.)(?<!\bSr\.)(?<!\bMrs\.)"

        # The gap itself, which is what gets removed by the split.
        r"\s+"
    )

    pieces = re.split(pattern, paragraph)

    # A paragraph that starts or ends with spaces produces empty pieces,
    # which are not sentences and should not be counted.
    sentences = []
    for piece in pieces:
        if piece.strip() != "":
            sentences.append(piece.strip())

    return sentences


def get_paragraph():
    """
    Asks the user to type a paragraph and returns it as a single string.

    Parameters:
        None

    Variables:
        lines (list of str): Every line the user has typed so far.
        line (str): The most recent line typed by the user.
        paragraph (str): All of the lines joined together with spaces.

    Logic:
        1. Explain how to enter the paragraph and how to finish.
        2. Loop, reading one line at a time.
        3. Stop when the user presses Enter on an empty line, but only after
           at least one line of text has been entered.
        4. Join the lines with spaces so a sentence can run across two lines.
        5. Return the paragraph.

    Return:
        str: The complete paragraph entered by the user.
    """
    print("Enter your paragraph below. You may use as many lines as you like.")
    print("Press Enter on an empty line when you are finished.")
    print()

    lines = []

    # Keep reading until the user signals the end with an empty line.
    while True:
        line = input("> ")

        # An empty line means the user is done, unless nothing has been
        # entered yet, because an empty paragraph has no sentences to show.
        if line.strip() == "":
            if len(lines) == 0:
                print("Please enter at least one line of text.")
            else:
                break
        else:
            lines.append(line.strip())

    # Joining with spaces lets a sentence that was typed across two lines
    # still be recognized as one sentence.
    paragraph = " ".join(lines)

    return paragraph


def display_sentences(sentences):
    """
    Displays each sentence on its own line and reports how many there are.

    Parameters:
        sentences (list of str): The sentences found in the paragraph.

    Variables:
        number (int): The position of the sentence being displayed.
        sentence (str): The sentence being displayed.
        word (str): The word "sentence" or "sentences", matched to the count.

    Logic:
        1. If the list is empty, say that no sentences were found and stop.
        2. Loop through the sentences, displaying each one with its number.
        3. Choose the singular or plural form of the word "sentence".
        4. Display the total count.

    Return:
        None
    """
    print()

    # An empty paragraph has nothing to number, so report that instead of
    # printing an empty list.
    if len(sentences) == 0:
        print("No sentences were found in the paragraph.")
        return

    print("The individual sentences in the paragraph:")

    # enumerate numbers the sentences for the user, starting at 1.
    for number, sentence in enumerate(sentences, 1):
        print(f"  Sentence {number}: {sentence}")

    # "1 sentences" would read poorly, so match the word to the count.
    if len(sentences) == 1:
        word = "sentence"
    else:
        word = "sentences"

    print()
    print(f"The paragraph contains {len(sentences)} {word}.")


def run_sentence_tests():
    """
    Splits known paragraphs and reports whether each one produced the
    expected sentences.

    Parameters:
        None

    Variables:
        test_cases (list of tuple): Each test as the paragraph to split, the
                                    sentences expected from it and a short
                                    note explaining what the case checks.
        passed (int): Accumulator counting the tests that produced the
                      expected sentences.
        paragraph (str): The paragraph being split by the current test.
        expected (list of str): The sentences the split should produce.
        note (str): What this case is checking.
        actual (list of str): The sentences the split actually produced.
        outcome (str): The word "PASS" or "FAIL" for the current test.

    Logic:
        1. Build the list of test cases, covering numbered sentences,
           decimals, abbreviations, quotes and missing punctuation.
        2. Set the passed accumulator to zero.
        3. Loop through the cases, splitting each paragraph.
        4. Compare the result with the expected sentences and report it.
        5. Add one to the accumulator for each test that passed.
        6. Display how many of the tests passed.

    Return:
        None
    """
    test_cases = [
        ("Hello there. How are you? I am fine!",
         ["Hello there.", "How are you?", "I am fine!"],
         "the three ending marks"),

        ("1. Alpha. 2. Beta. 3. Gamma.",
         ["1. Alpha.", "2. Beta.", "3. Gamma."],
         "every sentence begins with a number"),

        ("10. The tenth item is last.",
         ["10. The tenth item is last."],
         "a two-digit number begins the sentence"),

        ("The total was 3.5 million dollars. That is a lot.",
         ["The total was 3.5 million dollars.", "That is a lot."],
         "a decimal number is not a sentence ending"),

        ("1. The first item costs $3.50. 2. The second item is cheaper.",
         ["1. The first item costs $3.50.", "2. The second item is cheaper."],
         "a numbered sentence that also contains a decimal"),

        ("Mrs. Jones and Mr. Lee met St. Paul. They talked.",
         ["Mrs. Jones and Mr. Lee met St. Paul.", "They talked."],
         "abbreviations do not end a sentence"),

        ('"Stop right there." Then he left.',
         ['"Stop right there."', "Then he left."],
         "a closing quotation mark stays with its sentence"),

        ("No ending punctuation here",
         ["No ending punctuation here"],
         "a paragraph with no ending mark is one sentence"),

        ("   Leading and trailing spaces.   ",
         ["Leading and trailing spaces."],
         "surrounding spaces are removed"),

        ("One sentence only.",
         ["One sentence only."],
         "a single sentence"),
    ]

    print()
    print("Testing the sentence splitting on known paragraphs")
    print("=" * 70)

    # The accumulator starts at zero because no test has run yet.
    passed = 0

    for paragraph, expected, note in test_cases:
        actual = split_into_sentences(paragraph)

        # A test passes only when every sentence matches, in the same order.
        if actual == expected:
            outcome = "PASS"
            passed += 1
        else:
            outcome = "FAIL"

        print(f"{outcome}  {note}")
        print(f"      paragraph: {paragraph.strip()}")
        print(f"      sentences: {actual}")

    print("=" * 70)
    print(f"{passed} of {len(test_cases)} tests passed.")


def main():
    """
    Asks the user for a paragraph, then displays its sentences and the count.

    Parameters:
        None

    Variables:
        paragraph (str): The paragraph entered by the user.
        sentences (list of str): The sentences found in that paragraph.

    Logic:
        1. Display a title and an example of a numbered paragraph.
        2. Ask the user for the paragraph.
        3. Split the paragraph into sentences.
        4. Display the sentences and the count.

    Return:
        None
    """
    print("Paragraph Sentence Splitter")
    print("=" * 27)
    print("Sentences may begin with a number, as in: 1. The rent went up.")
    print()

    paragraph = get_paragraph()
    sentences = split_into_sentences(paragraph)
    display_sentences(sentences)


# Program entry point
if __name__ == "__main__":
    # Split the paragraph the user enters.
    main()

    # Show that the regular expression splits known paragraphs correctly.
    run_sentence_tests()
