def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    if num2 == 0:
        print("Error! Cannot divide by zero.")
        return None
    else:
        return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    if num2 == 0:
        print("Error! Cannot divide by zero.")
        return None
    else:
        return num1 / num2

def modulus(num1, num2):
    if num2 == 0:
        print("Error! Cannot divide by zero.")
        return None
    else:
        return num1 % num2


def main():
    while True:
        user_input = input("Enter an arithmetic operation (+, -, *, /) or 'q' to quit: ")

        if user_input.lower() == 'q':
            break

        try:
            # Extract numbers from input
            operator = user_input[0]
            num1_str = input("Enter the first number: ")
            num2_str = input("Enter the second number: ")

            try:
                num1 = float(num1_str)
                num2 = float(num2_str)

                if operator in ['+', '-', '*', '/']:
                    if operator == '+':
                        result = add(num1, num2)
                    elif operator == '-':
                        result = subtract(num1, num2)
                    elif operator == '*':
                        result = multiply(num1, num2)
                    else:
                        result = divide(num1, num2)
                    print(f"Result: {result}")
                else:
                    print("Invalid operation. Please try again.")
            except ValueError:
                print("Error! Invalid input.")
        except IndexError:
            print("Error! Invalid operation.")


if __name__ == "__main__":
    main()