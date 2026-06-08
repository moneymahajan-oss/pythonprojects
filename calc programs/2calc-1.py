# ============================================
# PROGRAM 2: Basic Calculator (+, -, *, /)
# Concepts: if/elif/else, operators
# ============================================

num1 = float(input("Enter first number : "))
op   = input("Enter operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))

if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
elif op == "*":
    result = num1 * num2
elif op == "/":
    if num2 == 0:
        result = "Error! Cannot divide by zero"
    else:
        result = num1 / num2
else:
    result = "Invalid operator!"

print("Answer:", result)
