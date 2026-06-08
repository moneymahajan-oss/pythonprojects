import customtkinter as ctk

# ─── App Theme ────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─── Main App Window ──────────────────────────────────────
app = ctk.CTk()
app.title("Calculator")
app.geometry("380x580")
app.resizable(False, False)

# ─── State Variables ──────────────────────────────────────
expression = ""
history = ""

# ─── Update Display ───────────────────────────────────────
def update_display(value):
    display_var.set(value)

def update_history(value):
    history_var.set(value)

# ─── Button Click Logic ───────────────────────────────────
def button_click(value):
    global expression

    if value == "C":
        expression = ""
        update_display("0")
        update_history("")

    elif value == "CE":
        expression = ""
        update_display("0")

    elif value == "⌫":
        expression = expression[:-1]
        update_display(expression if expression else "0")

    elif value == "=":
        try:
            update_history(expression + " =")
            result = eval(expression)
            # Show clean integer if result is whole number
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            update_display(str(result))
            expression = str(result)
        except ZeroDivisionError:
            update_display("Cannot divide by 0")
            expression = ""
        except Exception:
            update_display("Error")
            expression = ""

    elif value == "%":
        try:
            result = eval(expression) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            update_display(str(result))
            expression = str(result)
        except Exception:
            update_display("Error")
            expression = ""

    elif value == "1/x":
        try:
            result = 1 / eval(expression)
            update_display(str(round(result, 10)))
            expression = str(result)
        except ZeroDivisionError:
            update_display("Cannot divide by 0")
            expression = ""

    elif value == "x²":
        try:
            result = eval(expression) ** 2
            update_display(str(result))
            expression = str(result)
        except Exception:
            update_display("Error")
            expression = ""

    elif value == "√x":
        try:
            num = eval(expression)
            if num < 0:
                update_display("Invalid Input")
                expression = ""
            else:
                result = num ** 0.5
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                update_display(str(result))
                expression = str(result)
        except Exception:
            update_display("Error")
            expression = ""

    elif value == "+/-":
        try:
            result = eval(expression) * -1
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            update_display(str(result))
            expression = str(result)
        except Exception:
            update_display("Error")
            expression = ""

    elif value == ".":
        # Prevent multiple dots in the same number
        parts = expression.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
        if parts and "." in parts[-1]:
            return
        expression += value
        update_display(expression)

    else:
        # Prevent starting with operator
        if expression == "" and value in ["+", "*", "/"]:
            return
        expression += value
        update_display(expression)


# ─── Keyboard Support ─────────────────────────────────────
def key_press(event):
    key = event.char
    keysym = event.keysym

    if key in "0123456789":
        button_click(key)
    elif key == "+":
        button_click("+")
    elif key == "-":
        button_click("-")
    elif key == "*":
        button_click("*")
    elif key == "/":
        button_click("/")
    elif key == ".":
        button_click(".")
    elif key == "%":
        button_click("%")
    elif keysym == "Return":
        button_click("=")
    elif keysym == "BackSpace":
        button_click("⌫")
    elif keysym == "Escape":
        button_click("C")

app.bind("<Key>", key_press)

# ─── Display Area ─────────────────────────────────────────
display_frame = ctk.CTkFrame(app, fg_color="#1e1e1e", corner_radius=12)
display_frame.pack(fill="x", padx=15, pady=(15, 5))

history_var = ctk.StringVar(value="")
history_label = ctk.CTkLabel(
    display_frame,
    textvariable=history_var,
    font=ctk.CTkFont(size=13),
    text_color="#888888",
    anchor="e"
)
history_label.pack(fill="x", padx=15, pady=(10, 0))

display_var = ctk.StringVar(value="0")
display_label = ctk.CTkLabel(
    display_frame,
    textvariable=display_var,
    font=ctk.CTkFont(size=42, weight="bold"),
    text_color="white",
    anchor="e"
)
display_label.pack(fill="x", padx=15, pady=(0, 15))

# ─── Button Layout ────────────────────────────────────────
buttons_frame = ctk.CTkFrame(app, fg_color="transparent")
buttons_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Button grid layout — (text, row, col, colspan, color)
button_layout = [
    # Row 0 — special functions
    ("%",    0, 0, 1, "#2d2d2d"),
    ("CE",   0, 1, 1, "#2d2d2d"),
    ("C",    0, 2, 1, "#2d2d2d"),
    ("⌫",   0, 3, 1, "#2d2d2d"),

    # Row 1 — scientific
    ("1/x",  1, 0, 1, "#2d2d2d"),
    ("x²",   1, 1, 1, "#2d2d2d"),
    ("√x",   1, 2, 1, "#2d2d2d"),
    ("÷",    1, 3, 1, "#FF9500"),

    # Row 2
    ("7",    2, 0, 1, "#3a3a3a"),
    ("8",    2, 1, 1, "#3a3a3a"),
    ("9",    2, 2, 1, "#3a3a3a"),
    ("×",    2, 3, 1, "#FF9500"),

    # Row 3
    ("4",    3, 0, 1, "#3a3a3a"),
    ("5",    3, 1, 1, "#3a3a3a"),
    ("6",    3, 2, 1, "#3a3a3a"),
    ("-",    3, 3, 1, "#FF9500"),

    # Row 4
    ("1",    4, 0, 1, "#3a3a3a"),
    ("2",    4, 1, 1, "#3a3a3a"),
    ("3",    4, 2, 1, "#3a3a3a"),
    ("+",    4, 3, 1, "#FF9500"),

    # Row 5
    ("+/-",  5, 0, 1, "#3a3a3a"),
    ("0",    5, 1, 1, "#3a3a3a"),
    (".",    5, 2, 1, "#3a3a3a"),
    ("=",    5, 3, 1, "#0078D4"),
]

# Map display symbols to actual operators
operator_map = {
    "÷": "/",
    "×": "*",
}

def make_command(val):
    actual = operator_map.get(val, val)
    return lambda: button_click(actual)

# ─── Render All Buttons ───────────────────────────────────
for (text, row, col, colspan, color) in button_layout:
    actual_val = operator_map.get(text, text)
    btn = ctk.CTkButton(
        buttons_frame,
        text=text,
        font=ctk.CTkFont(size=18, weight="bold"),
        fg_color=color,
        hover_color="#555555" if color == "#3a3a3a" else (
            "#cc7a00" if color == "#FF9500" else
            "#005a9e" if color == "#0078D4" else "#444444"
        ),
        corner_radius=10,
        height=65,
        command=make_command(text)
    )
    btn.grid(
        row=row, column=col, columnspan=colspan,
        padx=5, pady=5, sticky="nsew"
    )

# Make grid responsive
for i in range(6):
    buttons_frame.grid_rowconfigure(i, weight=1)
for j in range(4):
    buttons_frame.grid_columnconfigure(j, weight=1)

# ─── Run App ──────────────────────────────────────────────
app.mainloop()
