# ============================================
# PROGRAM 4: OOP Calculator
# Concepts: class, __init__, methods, self
# ============================================

class Calculator:
    """A simple calculator class"""

    def __init__(self):
        """Called automatically when object is created"""
        self.history = []          # stores all calculations
        print("🧮 Calculator is ready!")

    # ── 4 Core Operations ──────────────────
    def add(self, a, b):
        result = a + b
        self._save(a, "+", b, result)
        return result

    def subtract(self, a, b):
        result = a - b
        self._save(a, "-", b, result)
        return result

    def multiply(self, a, b):
        result = a * b
        self._save(a, "*", b, result)
        return result

    def divide(self, a, b):
        if b == 0:
            print("❌ Error: Cannot divide by zero!")
            return None
        result = a / b
        self._save(a, "/", b, result)
        return result

    # ── Save to History ────────────────────
    def _save(self, a, op, b, result):
        entry = f"{a} {op} {b} = {result}"
        self.history.append(entry)

    # ── Show History ───────────────────────
    def show_history(self):
        if not self.history:
            print("No history yet.")
        else:
            print("\n📋 Calculation History:")
            for i, entry in enumerate(self.history, 1):
                print(f"  {i}. {entry}")

    # ── Main Menu ──────────────────────────
    def run(self):
        print("\n===== OOP Calculator =====")
        print("  +  -  *  /  h(history)  q(quit)")
        print("==========================\n")

        while True:
            try:
                num1 = input("First number (or 'q' to quit): ")
                if num1.lower() == "q":
                    self.show_history()
                    print("Goodbye! 👋")
                    break

                num1 = float(num1)
                op   = input("Operator (+, -, *, /, h): ").strip()

                if op == "h":
                    self.show_history()
                    continue

                num2   = float(input("Second number: "))
                result = None

                if   op == "+": result = self.add(num1, num2)
                elif op == "-": result = self.subtract(num1, num2)
                elif op == "*": result = self.multiply(num1, num2)
                elif op == "/": result = self.divide(num1, num2)
                else:
                    print("❌ Invalid operator!\n")
                    continue

                if result is not None:
                    print(f"✅ Answer: {result}\n")

            except ValueError:
                print("❌ Please enter a valid number!\n")


# ── Create object and run ──────────────────
calc = Calculator()
calc.run()
