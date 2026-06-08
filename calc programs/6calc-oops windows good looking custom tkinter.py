# ============================================
# PROGRAM 6: Full Fledged Standalone App
# pip install customtkinter
# Concepts: modern UI, themes, advanced OOP
# ============================================

import customtkinter as ctk
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FullCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calculator")
        self.geometry("380x580")
        self.resizable(False, False)

        self.expression = ""
        self.history    = ""

        self._build_display()
        self._build_buttons()

    # ── Display ────────────────────────────
    def _build_display(self):
        self.history_label = ctk.CTkLabel(
            self, text="", font=("Arial", 13),
            text_color="#888888", anchor="e", width=340
        )
        self.history_label.pack(padx=20, pady=(20, 0), anchor="e")

        self.display_label = ctk.CTkLabel(
            self, text="0", font=("Arial", 48, "bold"),
            text_color="white", anchor="e", width=340
        )
        self.display_label.pack(padx=20, pady=(0, 16), anchor="e")

    # ── Buttons ────────────────────────────
    def _build_buttons(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=16, pady=0, fill="both", expand=True)

        buttons = [
            ("%",   "sp"), ("CE",  "sp"), ("C",   "sp"), ("⌫",  "sp"),
            ("1/x", "sp"), ("x²",  "sp"), ("√x",  "sp"), ("÷",  "op"),
            ("7",   "nm"), ("8",   "nm"), ("9",   "nm"), ("×",  "op"),
            ("4",   "nm"), ("5",   "nm"), ("6",   "nm"), ("−",  "op"),
            ("1",   "nm"), ("2",   "nm"), ("3",   "nm"), ("+",  "op"),
            ("+/-", "sp"), ("0",   "nm"), (".",   "nm"), ("=",  "eq"),
        ]

        colors = {
            "nm": "#3a3a3c",
            "sp": "#636366",
            "op": "#FF9F0A",
            "eq": "#0A84FF",
        }

        for i, (label, style) in enumerate(buttons):
            row = i // 4
            col = i % 4
            ctk.CTkButton(
                frame,
                text             = label,
                font             = ("Arial", 20, "bold"),
                fg_color         = colors[style],
                hover_color      = colors[style],
                text_color       = "white",
                corner_radius    = 14,
                height           = 68,
                command          = lambda l=label: self.btn_click(l)
            ).grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            frame.grid_rowconfigure(i, weight=1)

    # ── Logic ──────────────────────────────
    def btn_click(self, value):
        expr = self.expression

        if value == "C":
            self.expression = ""
            self.history    = ""
            self._update("0", "")
        elif value == "CE":
            self.expression = ""
            self._update("0", self.history)
        elif value == "⌫":
            self.expression = expr[:-1]
            self._update(self.expression or "0", "")
        elif value == "=":
            try:
                self.history    = expr + " ="
                result          = eval(expr)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self._update(str(result), self.history)
            except ZeroDivisionError:
                self._update("Can't ÷ by 0", "")
                self.expression = ""
            except:
                self._update("Error", "")
                self.expression = ""
        elif value == "%":
            try:
                result = eval(expr) / 100
                self.expression = str(result)
                self._update(str(result), "")
            except: pass
        elif value == "1/x":
            try:
                result = round(1 / eval(expr), 10)
                self.expression = str(result)
                self._update(str(result), "")
            except: pass
        elif value == "x²":
            try:
                result = eval(expr) ** 2
                self.expression = str(result)
                self._update(str(result), "")
            except: pass
        elif value == "√x":
            try:
                result = math.sqrt(eval(expr))
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.expression = str(result)
                self._update(str(result), "")
            except: pass
        elif value == "+/-":
            try:
                result = eval(expr) * -1
                self.expression = str(result)
                self._update(str(result), "")
            except: pass
        elif value in ["÷", "×", "−", "+"]:
            symbol_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
            self.expression += symbol_map[value]
            self._update(self.expression, "")
        else:
            self.expression += value
            self._update(self.expression, "")

    def _update(self, display_text, history_text):
        self.display_label.configure(text=display_text)
        self.history_label.configure(text=history_text)


# ── Launch ─────────────────────────────────
app = FullCalculator()
app.mainloop()
