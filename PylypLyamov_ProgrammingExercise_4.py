"""
Name: Pylyp Lyamov
Date created: October 11, 2026
Course: COP2373 - Programming Exercise 4

Program description:
    This program checks whether a phone number, a Social Security number
    and a ZIP code are written in a valid format. Each value is checked by
    its own function using a regular expression. The main function asks the
    user for all three values and then displays whether each one is valid.
    After that, the program runs a set of built-in tests that feed known
    valid and invalid examples through the three functions, so the
    correctness of the regular expressions can be seen in the output.
"""

import re


def validate_phone_number(phone_number):
    """
    Checks whether a string is a valid United States phone number.

    Parameters:
        phone_number (str): The phone number entered by the user.

    Variables:
        pattern (str): The regular expression that describes a valid phone number.
        match (re.Match or None): The result of matching the pattern, or None.

    Logic:
        1. Build a pattern that allows an optional +1 country code.
        2. Allow either a parenthesized area code, such as (941) 555-0123,
           or a plain area code that uses the same separator twice, such as
           941-555-0123, 941.555.0123 or 9415550123.
        3. Require the area code and the exchange code to begin with a digit
           from 2 to 9, because no real area code starts with 0 or 1.
        4. Require exactly four digits at the end.
        5. Match the pattern against the whole string.
        6. Return True if the string matched and False if it did not.

    Return:
        bool: True when the phone number is valid, otherwise False.
    """
    # \1 repeats whatever separator was used the first time, so "941-555-0123"
    # is accepted but a mixed style such as "941-555.0123" is not.
    pattern = (
        r"^(?:\+1[ .-]?)?"                          # optional +1 country code
        r"(?:"
        r"\([2-9]\d{2}\) ?[2-9]\d{2}[ .-]?\d{4}"    # (941) 555-0123
        r"|"
        r"[2-9]\d{2}([ .-]?)[2-9]\d{2}\1\d{4}"      # 941-555-0123 or 9415550123
        r")$"
    )

    # fullmatch is not used here because the pattern already anchors itself
    # with ^ and $, which makes the rule visible inside the pattern.
    match = re.match(pattern, phone_number.strip())

    return match is not None


def validate_ssn(ssn):
    """
    Checks whether a string is a valid Social Security number.

    Parameters:
        ssn (str): The Social Security number entered by the user.

    Variables:
        pattern (str): The regular expression that describes a valid SSN.
        match (re.Match or None): The result of matching the pattern, or None.

    Logic:
        1. Build a pattern of three digits, two digits and four digits.
        2. Allow the three groups to be separated by a hyphen, a space or
           nothing at all, as long as the same separator is used both times.
        3. Reject an area number of 000 or 666, and any area number from 900
           to 999, because the Social Security Administration never issues them.
        4. Reject a group number of 00 and a serial number of 0000, which are
           never issued either.
        5. Match the pattern against the whole string.
        6. Return True if the string matched and False if it did not.

    Return:
        bool: True when the Social Security number is valid, otherwise False.
    """
    # (?!...) is a negative lookahead: it checks what comes next without
    # consuming it, which is how the never-issued numbers are ruled out.
    pattern = (
        r"^(?!000|666|9\d{2})\d{3}"   # area number, not 000, 666 or 900-999
        r"([ -]?)"                    # separator, remembered for reuse
        r"(?!00)\d{2}\1"              # group number, not 00, then same separator
        r"(?!0000)\d{4}$"             # serial number, not 0000
    )

    match = re.match(pattern, ssn.strip())

    return match is not None


def validate_zip_code(zip_code):
    """
    Checks whether a string is a valid United States ZIP code.

    Parameters:
        zip_code (str): The ZIP code entered by the user.

    Variables:
        pattern (str): The regular expression that describes a valid ZIP code.
        match (re.Match or None): The result of matching the pattern, or None.

    Logic:
        1. Build a pattern of exactly five digits.
        2. Allow an optional hyphen followed by exactly four more digits,
           which is the ZIP+4 form.
        3. Match the pattern against the whole string.
        4. Return True if the string matched and False if it did not.

    Return:
        bool: True when the ZIP code is valid, otherwise False.
    """
    # The group is optional as a whole, so both 34243 and 34243-1234 pass,
    # while a partial extension such as 34243-12 does not.
    pattern = r"^\d{5}(?:-\d{4})?$"

    match = re.match(pattern, zip_code.strip())

    return match is not None


def display_result(label, value, is_valid):
    """
    Displays whether one entered value is valid.

    Parameters:
        label (str): The name of the value, such as "Phone number".
        value (str): The text the user entered.
        is_valid (bool): True when the value is valid, otherwise False.

    Variables:
        verdict (str): The word "valid" or "not valid", chosen for this result.

    Logic:
        1. Choose the wording that matches the result.
        2. Display the label, the value entered and the verdict.

    Return:
        None
    """
    # A boolean prints as True or False, which reads poorly in a sentence,
    # so it is turned into words first.
    if is_valid:
        verdict = "valid"
    else:
        verdict = "not valid"

    print(f"{label}: {value} is {verdict}.")


def run_validation_tests():
    """
    Runs known valid and invalid examples through the three validation
    functions and reports whether each one produced the expected answer.

    Parameters:
        None

    Variables:
        test_cases (list of tuple): Each test as the function to call, the
                                    value to test, the expected answer and a
                                    short note explaining the case.
        passed (int): Accumulator counting the tests that produced the
                      expected answer.
        validator (function): The validation function used by the current test.
        value (str): The value being tested.
        expected (bool): The answer the function should return.
        note (str): The reason this case is valid or invalid.
        actual (bool): The answer the function actually returned.
        outcome (str): The word "PASS" or "FAIL" for the current test.

    Logic:
        1. Build the list of test cases, covering valid and invalid examples
           for all three validation functions.
        2. Set the passed accumulator to zero.
        3. Loop through the test cases, calling each validation function.
        4. Compare the answer with the expected answer and display the result.
        5. Add one to the accumulator for each test that passed.
        6. Display how many of the tests passed.

    Return:
        None
    """
    test_cases = [
        # Phone numbers that should be accepted.
        (validate_phone_number, "(941) 555-0123", True, "parentheses and a hyphen"),
        (validate_phone_number, "941-555-0123", True, "hyphens"),
        (validate_phone_number, "941.555.0123", True, "periods"),
        (validate_phone_number, "9415550123", True, "digits only"),
        (validate_phone_number, "+1 941-555-0123", True, "country code"),
        # Phone numbers that should be rejected.
        (validate_phone_number, "141-555-0123", False, "area code starts with 1"),
        (validate_phone_number, "941-555-012", False, "only three digits at the end"),
        (validate_phone_number, "(941 555-0123", False, "missing closing parenthesis"),
        (validate_phone_number, "941-555.0123", False, "separators do not match"),
        (validate_phone_number, "call me later", False, "not a number at all"),

        # Social Security numbers that should be accepted.
        (validate_ssn, "123-45-6789", True, "hyphens"),
        (validate_ssn, "123456789", True, "digits only"),
        # Social Security numbers that should be rejected.
        (validate_ssn, "000-45-6789", False, "area number 000 is never issued"),
        (validate_ssn, "666-45-6789", False, "area number 666 is never issued"),
        (validate_ssn, "900-45-6789", False, "area numbers above 899 are never issued"),
        (validate_ssn, "123-00-6789", False, "group number 00 is never issued"),
        (validate_ssn, "123-45-0000", False, "serial number 0000 is never issued"),
        (validate_ssn, "12-345-6789", False, "digits grouped incorrectly"),
        (validate_ssn, "123-45-678", False, "too few digits"),

        # ZIP codes that should be accepted.
        (validate_zip_code, "34243", True, "five digits"),
        (validate_zip_code, "34243-1234", True, "ZIP+4"),
        # ZIP codes that should be rejected.
        (validate_zip_code, "3424", False, "only four digits"),
        (validate_zip_code, "342431", False, "six digits"),
        (validate_zip_code, "34243-12", False, "incomplete ZIP+4"),
        (validate_zip_code, "ABCDE", False, "letters instead of digits"),
    ]

    print()
    print("Testing the validation functions with valid and invalid examples")
    print("=" * 72)

    # The accumulator starts at zero because no test has run yet.
    passed = 0

    for validator, value, expected, note in test_cases:
        actual = validator(value)

        # A test passes when the function agrees with the expected answer,
        # whether that answer is True or False.
        if actual == expected:
            outcome = "PASS"
            passed += 1
        else:
            outcome = "FAIL"

        print(f"{outcome}  {validator.__name__}({value!r}) returned {actual} - {note}")

    print("=" * 72)
    print(f"{passed} of {len(test_cases)} tests passed.")


def main():
    """
    Asks the user for a phone number, a Social Security number and a ZIP
    code, then displays whether each one is valid.

    Parameters:
        None

    Variables:
        phone_number (str): The phone number entered by the user.
        ssn (str): The Social Security number entered by the user.
        zip_code (str): The ZIP code entered by the user.

    Logic:
        1. Display a title and the accepted formats.
        2. Ask the user for each of the three values.
        3. Call the matching validation function for each value.
        4. Display whether each value is valid.

    Return:
        None
    """
    print("Phone Number, Social Security Number and ZIP Code Validator")
    print("=" * 58)
    print("Accepted formats:")
    print("  Phone number: (941) 555-0123, 941-555-0123, 941.555.0123 or 9415550123")
    print("  Social Security number: 123-45-6789 or 123456789")
    print("  ZIP code: 34243 or 34243-1234")
    print()

    phone_number = input("Enter a phone number: ")
    ssn = input("Enter a Social Security number: ")
    zip_code = input("Enter a ZIP code: ")

    print()

    # Each value is checked by the function written for that kind of value.
    display_result("Phone number", phone_number, validate_phone_number(phone_number))
    display_result("Social Security number", ssn, validate_ssn(ssn))
    display_result("ZIP code", zip_code, validate_zip_code(zip_code))


# Program entry point
if __name__ == "__main__":
    # Check the three values the user enters.
    main()

    # Show that the regular expressions are correct on known examples.
    run_validation_tests()
