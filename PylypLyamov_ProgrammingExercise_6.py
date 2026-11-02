"""
Name: Pylyp Lyamov
Date created: November 1, 2026
Course: COP2373 - Programming Exercise 6

Program description:
    This program stores the exam grades for a class in a CSV file and then
    displays them. The first part asks the instructor how many students to
    enter, then asks for each student's first name, last name and three exam
    grades. It uses the csv module to write the grades to a file named
    grades.csv, with a header row followed by one record per student. The
    second part reads grades.csv back with the csv module and displays the
    data as a table with aligned columns. Both parts open the file with the
    with keyword, which closes the file automatically when the work is done.
"""

import csv


def get_student_count():
    """
    Asks the instructor how many students they want to enter, and returns the
    number once it is a whole number of at least 1.

    Parameters:
        None

    Variables:
        response (str): The text the instructor typed at the prompt.

    Logic:
        1. Loop until the instructor enters a valid number.
        2. Prompt the instructor for the number of students.
        3. If the entry is made only of digits and is at least 1, return it
           as an integer.
        4. Otherwise, display a polite message and ask again.

    Return:
        int: The number of students to enter.
    """
    # Keep asking until the instructor types a number the program can use.
    while True:
        response = input("How many students would you like to enter? ").strip()

        # isdecimal() is True only when every character is a digit, so words,
        # negative numbers and decimals such as 2.5 are all turned away.
        if response.isdecimal() and int(response) >= 1:
            return int(response)

        # The entry failed the check, so show what is expected.
        print("Please enter a whole number of 1 or more.")


def get_name(prompt):
    """
    Asks for a name and returns it once something has been typed.

    Parameters:
        prompt (str): The question to display, such as "  First name: ".

    Variables:
        name (str): The name typed by the user, without surrounding spaces.

    Logic:
        1. Loop until the user enters a name.
        2. Display the prompt and read the name, removing surrounding spaces.
        3. If the name is not empty, return it.
        4. Otherwise, display a polite message and ask again.

    Return:
        str: The name entered by the user.
    """
    # Keep asking until the user types a name.
    while True:
        name = input(prompt).strip()

        # A blank name would leave an empty field in the grades file.
        if name != "":
            return name

        print("  Please enter a name.")


def get_exam_grade(exam_number):
    """
    Asks for a student's grade on one exam, and returns the grade once it is
    a whole number from 0 to 100.

    Parameters:
        exam_number (int): Which exam the grade is for: 1, 2 or 3.

    Variables:
        response (str): The text the user typed at the prompt.

    Logic:
        1. Loop until the user enters a valid grade.
        2. Prompt the user for the grade on this exam.
        3. If the entry is made only of digits and is no higher than 100,
           return it as an integer.
        4. Otherwise, display a polite message and ask again.

    Return:
        int: The exam grade, from 0 to 100.
    """
    # Keep asking until the user types a grade the program can use.
    while True:
        response = input(f"  Exam {exam_number} grade: ").strip()

        # Accepting only digits already rules out negative grades, so the top
        # of the scale is the only limit left to check.
        if response.isdecimal() and int(response) <= 100:
            return int(response)

        # The entry failed the check, so show what is expected.
        print("  Please enter a whole number from 0 to 100.")


def write_grades_file(file_name):
    """
    Asks the instructor for each student's name and exam grades, then uses the
    csv module to write them to the file: a header row first, followed by one
    record per student.

    Parameters:
        file_name (str): The name of the CSV file to create.

    Variables:
        student_count (int): The number of students the instructor will enter.
        records (list of list): One record per student: the first name, the
                                last name and the three exam grades.
        student_number (int): The number of the student being entered.
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        exam_grades (list of int): The student's grades on exams 1, 2 and 3.
        exam_number (int): The number of the exam being asked about.
        grades_file (file object): The CSV file, open for writing.
        writer (csv writer): Writes each list it is given as one line of the file.
        record (list): The student record being written to the file.

    Logic:
        1. Display a title and ask how many students will be entered.
        2. Loop once for each student, asking for the first name, the last
           name and the grades on exams 1, 2 and 3.
        3. Add each student's record to the list of records.
        4. Open the file for writing with the with keyword, which closes the
           file automatically at the end of the block.
        5. Use a csv writer to write the header row, then each record.
        6. Report how many records were written, matching the wording to the
           count.

    Return:
        None
    """
    print("Student Grade Entry")
    print("=" * 19)

    student_count = get_student_count()

    # Every record is collected before the file is opened, so the file is only
    # written once all of the instructor's input is complete.
    records = []

    for student_number in range(1, student_count + 1):
        print()
        print(f"Student {student_number} of {student_count}")

        first_name = get_name("  First name: ")
        last_name = get_name("  Last name: ")

        # The three exams are asked about in order, numbered 1 to 3.
        exam_grades = []
        for exam_number in range(1, 4):
            exam_grades.append(get_exam_grade(exam_number))

        records.append([first_name, last_name] + exam_grades)

    # The with keyword closes the file automatically when the block ends, even
    # if an error occurs. Mode "w" creates the file or replaces an older copy.
    # newline="" lets the csv module end each line itself (otherwise Windows
    # adds a blank line after every record), and UTF-8 can store a letter from
    # any language.
    with open(file_name, "w", newline="", encoding="utf-8") as grades_file:
        writer = csv.writer(grades_file)

        # The header row names the columns, so it is written first.
        writer.writerow(["First Name", "Last Name", "Exam 1", "Exam 2", "Exam 3"])

        # Each student becomes one record, which is one line of the file.
        for record in records:
            writer.writerow(record)

    # "1 student records were written" would read poorly, so match the wording
    # to the number of records.
    print()
    if student_count == 1:
        print(f"1 student record was written to {file_name}.")
    else:
        print(f"{student_count} student records were written to {file_name}.")


def read_grades_file(file_name):
    """
    Reads the CSV file with the csv module and displays its data as a table
    with aligned columns.

    Parameters:
        file_name (str): The name of the CSV file to read.

    Variables:
        title (str): The heading displayed above the table.
        grades_file (file object): The CSV file, open for reading.
        reader (csv reader): Splits each line of the file into a list of fields.
        rows (list of list): Every row in the file, starting with the header row.
        header (list of str): The column names from the first row.
        records (list of list): The student records that follow the header row.
        first_width (int): The width of the First Name column.
        last_width (int): The width of the Last Name column.
        dash_row (list of str): The line of dashes displayed under the headings.
        row (list of str): The row of the table being displayed.

    Logic:
        1. Display a heading for the table.
        2. Open the file for reading with the with keyword, which closes the
           file automatically at the end of the block.
        3. Use a csv reader to read every row of the file into a list.
        4. If the file does not exist or is empty, say so and stop.
        5. Separate the header row from the student records.
        6. Make each name column as wide as its longest entry plus two spaces,
           so that a long name cannot push the grades out of line.
        7. Display the header, a line of dashes under it and every record,
           with the names left-aligned and the grades right-aligned in columns
           8 characters wide.

    Return:
        None
    """
    title = f"Student Grades in {file_name}"

    print()
    print(title)
    print("=" * len(title))

    # The file will not exist if this part runs before any grades have been
    # entered, so that case is reported instead of stopping with an error.
    try:
        # The with keyword closes the file as soon as reading is finished, so
        # every row is read into a list while the file is still open.
        with open(file_name, "r", newline="", encoding="utf-8") as grades_file:
            reader = csv.reader(grades_file)
            rows = list(reader)
    except FileNotFoundError:
        print(f"The file {file_name} does not exist yet. Please enter some grades first.")
        return

    # An empty file has neither a header nor any records to show.
    if len(rows) == 0:
        print(f"The file {file_name} is empty.")
        return

    header = rows[0]
    records = rows[1:]

    # Each name column is as wide as its longest entry, counting the heading,
    # plus two spaces to separate it from the next column.
    first_width = max(len(row[0]) for row in rows) + 2
    last_width = max(len(row[1]) for row in rows) + 2

    # A line of dashes under the headings separates them from the records.
    dash_row = ["-" * (first_width - 2), "-" * (last_width - 2), "-" * 6, "-" * 6, "-" * 6]

    # In each format specification, < left-aligns and > right-aligns the value
    # in a column of the given width. The name columns get their widths from
    # first_width and last_width, because those are only known at run time.
    for row in [header, dash_row] + records:
        print(f"{row[0]:<{first_width}}{row[1]:<{last_width}}"
              f"{row[2]:>8}{row[3]:>8}{row[4]:>8}")


def main():
    """
    Runs both parts of the program: entering the grades into the CSV file,
    then reading the file back and displaying it as a table.

    Parameters:
        None

    Variables:
        file_name (str): The name of the CSV file that both parts use.

    Logic:
        1. Set the name of the CSV file to grades.csv.
        2. Call write_grades_file to collect the grades and create the file.
        3. Call read_grades_file to read the file and display it as a table.

    Return:
        None
    """
    # Both parts work with the same file, so its name is set in one place.
    file_name = "grades.csv"

    # Part 1: enter the students' grades and write them to the file.
    write_grades_file(file_name)

    # Part 2: read the file back and display its data as a table.
    read_grades_file(file_name)


# Program entry point
if __name__ == "__main__":
    main()
