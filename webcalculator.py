import streamlit as st

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

st.markdown("""
<style>
/* Hide Streamlit UI */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    max-width: 420px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Background */
.stApp { background-color: #1c1c1e; }

/* Display */
.calc-display {
    background: #2c2c2e;
    border-radius: 16px;
    padding: 24px 20px 16px 20px;
    text-align: right;
    margin-bottom: 16px;
    min-height: 110px;
}
.calc-history {
    color: #888;
    font-size: 15px;
    min-height: 22px;
    margin-bottom: 4px;
}
.calc-result {
    color: #ffffff;
    font-size: 52px;
    font-weight: 700;
    word-break: break-all;
    line-height: 1.1;
}

/* All buttons base */
div.stButton > button {
    width: 100% !important;
    height: 70px !important;
    font-size: 22px !important;
    font-weight: 600 !important;
    border-radius: 14px !important;
    border: none !important;
    background-color: #3a3a3c !important;
    color: #ffffff !important;
    transition: all 0.15s ease !important;
    margin: 2px 0 !important;
}
div.stButton > button:hover {
    background-color: #545458 !important;
    color: #ffffff !important;
}
div.stButton > button:active {
    transform: scale(0.95) !important;
}

/* Operator buttons - Orange */
.op div.stButton > button {
    background-color: #FF9F0A !important;
    color: #ffffff !important;
}
.op div.stButton > button:hover {
    background-color: #FFB340 !important;
    color: #ffffff !important;
}

/* Equals button - Blue */
.eq div.stButton > button {
    background-color: #0A84FF !important;
    color: #ffffff !important;
}
.eq div.stButton > button:hover {
    background-color: #409CFF !important;
    color: #ffffff !important;
}

/* Special top row - Dark Gray */
.sp div.stButton > button {
    background-color: #636366 !important;
    color: #ffffff !important;
    font-size: 18px !important;
}
.sp div.stButton > button:hover {
    background-color: #7c7c80 !important;
    color: #ffffff !important;
}

/* Remove gap between columns */
[data-testid="column"] {
    padding: 3px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────
for key, val in [("expression", ""), ("display", "0"), ("history", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Button Logic ───────────────────────────────────────────
def btn_click(value):
    expr = st.session_state.expression

    if value == "C":
        st.session_state.expression = ""
        st.session_state.display   = "0"
        st.session_state.history   = ""

    elif value == "CE":
        st.session_state.expression = ""
        st.session_state.display    = "0"

    elif value == "⌫":
        expr = expr[:-1]
        st.session_state.expression = expr
        st.session_state.display    = expr if expr else "0"

    elif value == "=":
        try:
            st.session_state.history    = expr + "  ="
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except ZeroDivisionError:
            st.session_state.display    = "Can't ÷ by 0"
            st.session_state.expression = ""
        except:
            st.session_state.display    = "Error"
            st.session_state.expression = ""

    elif value == "%":
        try:
            result = eval(expr) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == "1/x":
        try:
            result = 1 / eval(expr)
            st.session_state.display    = str(round(result, 10))
            st.session_state.expression = str(result)
        except ZeroDivisionError:
            st.session_state.display    = "Can't ÷ by 0"
            st.session_state.expression = ""

    elif value == "x²":
        try:
            result = eval(expr) ** 2
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"

    elif value == "√x":
        try:
            num = eval(expr)
            if num < 0:
                st.session_state.display    = "Invalid"
                st.session_state.expression = ""
            else:
                result = num ** 0.5
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                st.session_state.display    = str(result)
                st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"

    elif value == "+/-":
        try:
            result = eval(expr) * -1
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"

    elif value == ".":
        parts = expr.replace("+", " ").replace("-", " ")\
                    .replace("*", " ").replace("/", " ").split()
        if parts and "." in parts[-1]:
            return
        new = expr + value
        st.session_state.expression = new
        st.session_state.display    = new

    else:
        if expr == "" and value in ["+", "*", "/"]:
            return
        new = expr + value
        st.session_state.expression = new
        st.session_state.display    = new

# ── Display ────────────────────────────────────────────────
st.markdown(f"""
<div class="calc-display">
    <div class="calc-history">{st.session_state.history}&nbsp;</div>
    <div class="calc-result">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# ── Helper to render button with style class ───────────────
def render(col, label, key, style="", click_val=None):
    with col:
        if style:
            st.markdown(f'<div class="{style}">', unsafe_allow_html=True)
        if st.button(label, key=key):
            btn_click(click_val or label)
        if style:
            st.markdown('</div>', unsafe_allow_html=True)

# ── Row 1 — Special Functions ──────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "%",  "pct",  "sp", "%")
render(c[1], "CE", "ce",   "sp", "CE")
render(c[2], "C",  "cl",   "sp", "C")
render(c[3], "⌫",  "back", "sp", "⌫")

# ── Row 2 — Scientific ─────────────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "1/x", "inv",  "sp",  "1/x")
render(c[1], "x²",  "sq",   "sp",  "x²")
render(c[2], "√x",  "sqrt", "sp",  "√x")
render(c[3], "÷",   "div",  "op",  "/")

# ── Row 3 — 7 8 9 × ───────────────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "7", "n7", "", "7")
render(c[1], "8", "n8", "", "8")
render(c[2], "9", "n9", "", "9")
render(c[3], "×", "mul", "op", "*")

# ── Row 4 — 4 5 6 − ───────────────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "4", "n4", "", "4")
render(c[1], "5", "n5", "", "5")
render(c[2], "6", "n6", "", "6")
render(c[3], "−", "sub", "op", "-")

# ── Row 5 — 1 2 3 + ───────────────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "1", "n1", "", "1")
render(c[1], "2", "n2", "", "2")
render(c[2], "3", "n3", "", "3")
render(c[3], "+", "add", "op", "+")

# ── Row 6 — +/- 0 . = ─────────────────────────────────────
c = st.columns(4, gap="small")
render(c[0], "+/-", "neg", "sp",  "+/-")
render(c[1], "0",   "n0",  "",    "0")
render(c[2], ".",   "dot", "",    ".")
render(c[3], "=",   "eq",  "eq",  "=")
