"""
Name: Pylyp Lyamov
Date created: August 30, 2026
Course: COP2373 - Debugging Exercise

Program description:
    This program prints the discounted price of every product in a list.

    The original version crashed with "TypeError: can't multiply sequence by
    non-int of type 'float'" because the Tablet stored its price as the text
    "500" instead of the number 500. This version converts each value to a
    number before the arithmetic, and reports any value that cannot be used
    as a number instead of stopping the whole program.
"""


def to_number(value, field_name, product_name):
    """Converts a product value to a float, or raises ValueError explaining why it cannot."""
    # A missing key arrives here as None, which deserves its own wording
    # because "is not a number" would not tell the user what to fix.
    if value is None:
        raise ValueError(f"the {field_name} is missing")

    # float() accepts an int, a float or numeric text such as "500", which is
    # what the product list actually contained.
    try:
        return float(value)

    # A missing value raises TypeError and non-numeric text raises ValueError,
    # so both are turned into one message that names the product and the field.
    except (TypeError, ValueError):
        raise ValueError(f"the {field_name} is {value!r}, which is not a number")


def calculate_discount(price, discount_rate):
    """Calculates the discount amount based on the price and discount rate."""
    discount_amount = price * discount_rate
    return discount_amount


def apply_discount(price, discount_amount):
    """Applies the discount amount to the original price and returns the new price."""
    new_price = price - discount_amount
    return new_price


def show_product_pricing(product):
    """Prints the pricing for one product, or a message if its data cannot be used."""
    # A product with no name should still produce a readable message.
    product_name = product.get("name", "an unnamed product")

    # Both values are converted here, before any arithmetic, because this is
    # the point where bad data enters the calculation.
    try:
        price = to_number(product.get("price"), "price", product_name)
        discount_rate = to_number(product.get("discount_rate"), "discount rate", product_name)

    # One unusable product should not stop the remaining products from printing.
    except ValueError as error:
        print(f"Cannot price {product_name}: {error}.")
        print()
        return False

    discount_amount = calculate_discount(price, discount_rate)
    final_price = apply_discount(price, discount_amount)

    # Money is displayed to two decimal places so the amounts read as currency.
    print(f"Product: {product_name}")
    print(f"Original Price: ${price:.2f}")
    print(f"Discount Amount: ${discount_amount:.2f}")
    print(f"Final Price: ${final_price:.2f}")
    print()

    return True


def main():
    """Prints the pricing for every product in the original product list."""
    products = [
        {"name": "Laptop", "price": 1000, "discount_rate": 0.1},
        {"name": "Smartphone", "price": 800, "discount_rate": 0.15},
        {"name": "Tablet", "price": "500", "discount_rate": 0.2},
        {"name": "Headphones", "price": 200, "discount_rate": 0.05}
    ]

    # The Tablet price is still the text "500" exactly as it was given, which
    # shows that the program now handles it instead of crashing on it.
    for product in products:
        show_product_pricing(product)


def test_error_handling():
    """Runs deliberately incorrect data through the program to show the error handling."""
    broken_products = [
        {"name": "Monitor", "price": "free", "discount_rate": 0.1},
        {"name": "Keyboard", "price": None, "discount_rate": 0.1},
        {"name": "Mouse", "price": 50, "discount_rate": "ten percent"},
        {"name": "Webcam", "discount_rate": 0.1}
    ]

    print("Error handling tests: the products below contain deliberately bad data.")
    print()

    # Every one of these should print a message and none should crash.
    for product in broken_products:
        show_product_pricing(product)

    print("All four bad products were reported and the program kept running.")


# Program entry point
if __name__ == "__main__":
    # Print the pricing for the original product list.
    main()

    # Show that incorrect values are handled with a meaningful message.
    test_error_handling()
