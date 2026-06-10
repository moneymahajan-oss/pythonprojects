# ============================================
# PROGRAM 7: Web Calculator — Streamlit
# Deploy on Streamlit Cloud
# ============================================

import streamlit as st
import math

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #1c1c1e; }
.block-container { padding-top: 1rem !important; }
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 14px;
    border: none;
    color: white !important;
    background-color: #3a3a3c;
    transition: filter 0.1s;
}
div.stButton > button:hover { filter: brightness(1.3); color: white !important; }
div.stButton > button:active { filter: brightness(1.5); color: white !important; }
.calc-display {
    background-color: #2c2c2e;
    border-radius: 16px;
    padding: 16px 24px 12px;
    margin-bottom: 16px;
    text-align: right;
}
.calc-history { color: #888888; font-size: 15px; min-height: 22px; font-family: Arial; }
.calc-number  { color: white; font-size: 52px; font-weight: bold; font-family: Arial; line-height: 1.1; word-break: break-all; }
</style>
""", unsafe_allow_html=True)

# ── Session State ───────────────────────────
for k, v in {"expression": "", "display": "0", "history": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Button Logic ────────────────────────────
def btn_click(value):
    expr = st.session_state.expression

    if value == "C":
        st.session_state.expression = ""
        st.session_state.display    = "0"
        st.session_state.history    = ""
    elif value == "CE":
        st.session_state.expression = ""
        st.session_state.display    = "0"
    elif value == "⌫":
        st.session_state.expression = expr[:-1]
        st.session_state.display    = st.session_state.expression or "0"
    elif value == "=":
        try:
            st.session_state.history = expr + " ="
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
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except: pass
    elif value == "1/x":
        try:
            result = round(1 / eval(expr), 10)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except: pass
    elif value == "x²":
        try:
            result = eval(expr) ** 2
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except: pass
    elif value == "√x":
        try:
            result = math.sqrt(eval(expr))
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except: pass
    elif value == "+/-":
        try:
            result = eval(expr) * -1
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except: pass
    elif value in ["÷", "×", "−", "+"]:
        symbol_map = {"÷": "/", "×": "*", "−": "-", "+": "+"}
        st.session_state.expression += symbol_map[value]
        st.session_state.display     = st.session_state.expression
    else:
        st.session_state.expression += value
        st.session_state.display     = st.session_state.expression

# ── UI ──────────────────────────────────────
@st.fragment
def calculator():
    st.markdown(f"""
    <div class="calc-display">
        <div class="calc-history">{st.session_state.history}</div>
        <div class="calc-number">{st.session_state.display}</div>
    </div>
    """, unsafe_allow_html=True)

    btn_styles = {"sp":"#636366","nm":"#3a3a3c","op":"#FF9F0A","eq":"#0A84FF"}
    buttons = [
        ("%","sp"),("CE","sp"),("C","sp"),("⌫","sp"),
        ("1/x","sp"),("x²","sp"),("√x","sp"),("÷","op"),
        ("7","nm"),("8","nm"),("9","nm"),("×","op"),
        ("4","nm"),("5","nm"),("6","nm"),("−","op"),
        ("1","nm"),("2","nm"),("3","nm"),("+","op"),
        ("+/-","sp"),("0","nm"),(".","nm"),("=","eq"),
    ]

    color_css = ""
    for i,(label,style) in enumerate(buttons):
        color = btn_styles[style]
        color_css += f"""
        div[data-testid="stHorizontalBlock"] > div:nth-child({(i%4)+1}) div.stButton > button {{
            background-color: {color};
        }}"""
    st.markdown(f"<style>{color_css}</style>", unsafe_allow_html=True)

    for row_start in range(0, 24, 4):
        cols = st.columns(4)
        for col_idx, col in enumerate(cols):
            label, style = buttons[row_start + col_idx]
            with col:
                if st.button(label, key=f"btn_{row_start}_{col_idx}",
                             use_container_width=True):
                    btn_click(label)

calculator()
