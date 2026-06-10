# ============================================
# PROGRAM 5: Windows Desktop Calculator
# Concepts: tkinter, GUI, grid layout, events
# ============================================

import tkinter as tk

class CalculatorApp:
    def __init__(self, root):
        self.root       = root
        self.expression = ""
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c1e")

        # ── Display Screen ─────────────────
        self.display_var = tk.StringVar(value="0")
        self.history_var = tk.StringVar(value="")

        tk.Label(
            root, textvariable=self.history_var,
            font=("Arial", 12), bg="#2c2c2e", fg="#888888",
            anchor="e", width=24
        ).grid(row=0, column=0, columnspan=4,
               padx=10, pady=(10,0), sticky="ew")

        tk.Label(
            root, textvariable=self.display_var,
            font=("Arial", 28, "bold"), bg="#2c2c2e", fg="white",
            anchor="e", width=24
        ).grid(row=1, column=0, columnspan=4,
               padx=10, pady=(0,10), sticky="ew")

        # ── Button Layout ──────────────────
        buttons = [
            ("%",   "sp"), ("CE",  "sp"), ("C",   "sp"), ("⌫",  "sp"),
            ("1/x", "sp"), ("x²",  "sp"), ("√x",  "sp"), ("÷",  "op"),
            ("7",   "nm"), ("8",   "nm"), ("9",   "nm"), ("×",  "op"),
            ("4",   "nm"), ("5",   "nm"), ("6",   "nm"), ("−",  "op"),
            ("1",   "nm"), ("2",   "nm"), ("3",   "nm"), ("+",  "op"),
            ("+/-", "sp"), ("0",   "nm"), (".",   "nm"), ("=",  "eq"),
        ]

        colors = {
            "nm": ("#3a3a3c", "white"),
            "sp": ("#636366", "white"),
            "op": ("#FF9F0A", "white"),
            "eq": ("#0A84FF", "white"),
        }

        for i, (label, style) in enumerate(buttons):
            bg, fg = colors[style]
            row = (i // 4) + 2
            col = i % 4
            btn = tk.Button(
                root,
                text    = label,
                font    = ("Arial", 16, "bold"),
                bg      = bg,
                fg      = fg,
                width   = 5,
                height  = 2,
                bd      = 0,
                relief  = "flat",
                cursor  = "hand2",
                activebackground = bg,
                activeforeground = fg,
                command = lambda l=label: self.btn_click(l)
            )
            btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")

        # Make all columns and rows expand equally
        for c in range(4):
            root.columnconfigure(c, weight=1)
        for r in range(2, 8):
            root.rowconfigure(r, weight=1)

    # ── Button Logic ───────────────────────
    def btn_click(self, value):
        expr = self.expression

        if value == "C":
            self.expression = ""
            self.display_var.set("0")
            self.history_var.set("")
        elif value == "CE":
            self.expression = ""
            self.display_var.set("0")
        elif value == "⌫":
            self.expression = expr[:-1]
            self.display_var.set(self.expression or "0")
        elif value == "=":
            try:
                self.history_var.set(expr + " =")
                result = eval(expr)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.display_var.set(str(result))
                self.expression = str(result)
            except ZeroDivisionError:
                self.display_var.set("Can't divide by 0")
                self.expression = ""
            except:
                self.display_var.set("Error")
                self.expression = ""
        elif value == "%":
            try:
                result = eval(expr) / 100
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                pass
        elif value == "1/x":
            try:
                result = 1 / eval(expr)
                self.display_var.set(str(round(result, 10)))
                self.expression = str(result)
            except:
                pass
        elif value == "x²":
            try:
                result = eval(expr) ** 2
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                pass
        elif value == "√x":
            try:
                num = eval(expr)
                result = num ** 0.5
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                pass
        elif value == "+/-":
            try:
                result = eval(expr) * -1
                self.display_var.set(str(result))
                self.expression = str(result)
            except:
                pass
        elif value in ["÷", "×", "−", "+"]:
            symbol_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
            self.expression += symbol_map[value]
            self.display_var.set(self.expression)
        else:
            self.expression += value
            self.display_var.set(self.expression)


# ── Launch App ─────────────────────────────
root = tk.Tk()
root.geometry("380x550")
root.resizable(False, False)
app  = CalculatorApp(root)
root.mainloop()
