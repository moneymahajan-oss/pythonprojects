import streamlit as st

# ─── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

# ─── Custom CSS Styling ───────────────────────────────────
st.markdown("""
<style>
    /* Background */
    .stApp {
        background-color: #1e1e1e;
    }

    /* Display box */
    .calc-display {
        background-color: #2d2d2d;
        border-radius: 12px;
        padding: 20px;
        text-align: right;
        margin-bottom: 20px;
    }

    .calc-history {
        color: #888888;
        font-size: 14px;
        min-height: 20px;
    }

    .calc-result {
        color: white;
        font-size: 48px;
        font-weight: bold;
        word-break: break-all;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        height: 65px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        background-color: #3a3a3a;
        color: white;
        cursor: pointer;
        transition: background-color 0.2s;
    }

    div.stButton > button:hover {
        background-color: #555555;
        color: white;
    }

    /* Operator buttons */
    .op-btn > div.stButton > button {
        background-color: #FF9500;
    }
    .op-btn > div.stButton > button:hover {
        background-color: #cc7a00;
    }

    /* Equal button */
    .eq-btn > div.stButton > button {
        background-color: #0078D4;
    }
    .eq-btn > div.stButton > button:hover {
        background-color: #005a9e;
    }

    /* Special buttons */
    .sp-btn > div.stButton > button {
        background-color: #2d2d2d;
    }
    .sp-btn > div.stButton > button:hover {
        background-color: #444444;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Center everything */
    .block-container {
        max-width: 400px;
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "display" not in st.session_state:
    st.session_state.display = "0"
if "history" not in st.session_state:
    st.session_state.history = ""

# ─── Button Logic ─────────────────────────────────────────
def btn_click(value):
    expr = st.session_state.expression

    if value == "C":
        st.session_state.expression = ""
        st.session_state.display = "0"
        st.session_state.history = ""

    elif value == "CE":
        st.session_state.expression = ""
        st.session_state.display = "0"

    elif value == "⌫":
        expr = expr[:-1]
        st.session_state.expression = expr
        st.session_state.display = expr if expr else "0"

    elif value == "=":
        try:
            st.session_state.history = expr + " ="
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display = str(result)
            st.session_state.expression = str(result)
        except ZeroDivisionError:
            st.session_state.display = "Cannot divide by 0"
            st.session_state.expression = ""
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == "%":
        try:
            result = eval(expr) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == "1/x":
        try:
            result = 1 / eval(expr)
            st.session_state.display = str(round(result, 10))
            st.session_state.expression = str(result)
        except ZeroDivisionError:
            st.session_state.display = "Cannot divide by 0"
            st.session_state.expression = ""

    elif value == "x²":
        try:
            result = eval(expr) ** 2
            st.session_state.display = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == "√x":
        try:
            num = eval(expr)
            if num < 0:
                st.session_state.display = "Invalid Input"
                st.session_state.expression = ""
            else:
                result = num ** 0.5
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                st.session_state.display = str(result)
                st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == "+/-":
        try:
            result = eval(expr) * -1
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
            st.session_state.expression = ""

    elif value == ".":
        parts = expr.replace("+", " ").replace("-", " ").replace("*", " ").replace("/", " ").split()
        if parts and "." in parts[-1]:
            return
        st.session_state.expression = expr + value
        st.session_state.display = expr + value

    else:
        if expr == "" and value in ["+", "*", "/"]:
            return
        st.session_state.expression = expr + value
        st.session_state.display = expr + value

# ─── Display ──────────────────────────────────────────────
st.markdown(f"""
<div class="calc-display">
    <div class="calc-history">{st.session_state.history}&nbsp;</div>
    <div class="calc-result">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)

# ─── Button Grid ──────────────────────────────────────────
# Row 1 — Special
r1 = st.columns(4)
with r1[0]: 
    with st.container():
        st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
        if st.button("%", key="pct"): btn_click("%")
        st.markdown('</div>', unsafe_allow_html=True)
with r1[1]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("CE", key="ce"): btn_click("CE")
    st.markdown('</div>', unsafe_allow_html=True)
with r1[2]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("C", key="c"): btn_click("C")
    st.markdown('</div>', unsafe_allow_html=True)
with r1[3]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("⌫", key="back"): btn_click("⌫")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2 — Scientific
r2 = st.columns(4)
with r2[0]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("1/x", key="inv"): btn_click("1/x")
    st.markdown('</div>', unsafe_allow_html=True)
with r2[1]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("x²", key="sq"): btn_click("x²")
    st.markdown('</div>', unsafe_allow_html=True)
with r2[2]:
    st.markdown('<div class="sp-btn">', unsafe_allow_html=True)
    if st.button("√x", key="sqrt"): btn_click("√x")
    st.markdown('</div>', unsafe_allow_html=True)
with r2[3]:
    st.markdown('<div class="op-btn">', unsafe_allow_html=True)
    if st.button("÷", key="div"): btn_click("/")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 3 — 7 8 9
r3 = st.columns(4)
with r3[0]:
    if st.button("7", key="7"): btn_click("7")
with r3[1]:
    if st.button("8", key="8"): btn_click("8")
with r3[2]:
    if st.button("9", key="9"): btn_click("9")
with r3[3]:
    st.markdown('<div class="op-btn">', unsafe_allow_html=True)
    if st.button("×", key="mul"): btn_click("*")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 4 — 4 5 6
r4 = st.columns(4)
with r4[0]:
    if st.button("4", key="4"): btn_click("4")
with r4[1]:
    if st.button("5", key="5"): btn_click("5")
with r4[2]:
    if st.button("6", key="6"): btn_click("6")
with r4[3]:
    st.markdown('<div class="op-btn">', unsafe_allow_html=True)
    if st.button("-", key="sub"): btn_click("-")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 5 — 1 2 3
r5 = st.columns(4)
with r5[0]:
    if st.button("1", key="1"): btn_click("1")
with r5[1]:
    if st.button("2", key="2"): btn_click("2")
with r5[2]:
    if st.button("3", key="3"): btn_click("3")
with r5[3]:
    st.markdown('<div class="op-btn">', unsafe_allow_html=True)
    if st.button("+", key="add"): btn_click("+")
    st.markdown('</div>', unsafe_allow_html=True)

# Row 6 — 0 . =
r6 = st.columns(4)
with r6[0]:
    if st.button("+/-", key="neg"): btn_click("+/-")
with r6[1]:
    if st.button("0", key="0"): btn_click("0")
with r6[2]:
    if st.button(".", key="dot"): btn_click(".")
with r6[3]:
    st.markdown('<div class="eq-btn">', unsafe_allow_html=True)
    if st.button("=", key="eq"): btn_click("=")
    st.markdown('</div>', unsafe_allow_html=True)
