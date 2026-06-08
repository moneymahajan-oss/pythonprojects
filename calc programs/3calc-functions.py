# ============================================
# PROGRAM 3: Calculator with Loop + Functions
# Concepts: functions, while loop, try/except
# ============================================

def add(a, b):      return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        return "Error! Cannot divide by zero"
    return a / b

def calculate():
    print("\n===== Simple Calculator =====")
    print("  Operators: +  -  *  /  ")
    print("  Type 'exit' to quit     ")
    print("=============================\n")

    while True:
        try:
            num1 = input("Enter first number (or 'exit'): ")
            if num1.lower() == "exit":
                print("Goodbye! 👋")
                break

            num1 = float(num1)
            op   = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number        : "))

            if   op == "+": result = add(num1, num2)
            elif op == "-": result = subtract(num1, num2)
            elif op == "*": result = multiply(num1, num2)
            elif op == "/": result = divide(num1, num2)
            else:
                print("❌ Invalid operator! Try again.\n")
                continue

            print(f"✅ Answer: {num1} {op} {num2} = {result}\n")

        except ValueError:
            print("❌ Please enter a valid number!\n")

# Run the program
calculate()
