import streamlit as st

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

# ── Session State ──────────────────────────────────────────
for key, val in [("expression", ""), ("display", "0"), ("history", "")]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Button Logic ───────────────────────────────────────────
def btn_click(value):
    expr = st.session_state.expression

    if value == "C":
        st.session_state.expression = ""
        st.session_state.display    = "0"
        st.session_state.history    = ""

    elif value == "CE":
        st.session_state.expression = ""
        st.session_state.display    = "0"

    elif value == "DEL":
        expr = expr[:-1]
        st.session_state.expression = expr
        st.session_state.display    = expr if expr else "0"

    elif value == "=":
        try:
            st.session_state.history    = expr + " ="
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

    elif value == "PCT":
        try:
            result = eval(expr) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display    = "Error"
            st.session_state.expression = ""

    elif value == "INV":
        try:
            result = 1 / eval(expr)
            st.session_state.display    = str(round(result, 10))
            st.session_state.expression = str(result)
        except ZeroDivisionError:
            st.session_state.display    = "Can't ÷ by 0"
            st.session_state.expression = ""

    elif value == "SQ":
        try:
            result = eval(expr) ** 2
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"

    elif value == "SQRT":
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

    elif value == "NEG":
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


# ── Styling ────────────────────────────────────────────────
st.markdown("""
<style>
/* Hide Streamlit chrome */
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    max-width: 400px !important;
    padding-top: 1rem !important;
}
.stApp { background-color: #1c1c1e; }

/* Display box */
.calc-display {
    background: #2c2c2e;
    border-radius: 16px;
    padding: 20px 18px 14px;
    text-align: right;
    margin-bottom: 12px;
    min-height: 100px;
}
.calc-history {
    color: #888;
    font-size: 14px;
    min-height: 20px;
    margin-bottom: 4px;
}
.calc-result {
    color: #fff;
    font-size: 48px;
    font-weight: 700;
    word-break: break-all;
}

/* Universal button reset */
[data-testid="stButton"] button {
    width: 100% !important;
    height: 68px !important;
    font-size: 20px !important;
    font-weight: 600 !important;
    border-radius: 14px !important;
    border: none !important;
    cursor: pointer !important;
    transition: filter 0.15s !important;
}
[data-testid="stButton"] button:hover {
    filter: brightness(1.3) !important;
}

/* Normal number buttons */
[data-testid="stButton"] button[kind="secondary"] {
    background-color: #3a3a3c !important;
    color: #ffffff !important;
}

/* Row gap */
[data-testid="column"] { padding: 2px 3px !important; }
</style>
""", unsafe_allow_html=True)


# ── Display ────────────────────────────────────────────────
st.markdown(f"""
<div class="calc-display">
    <div class="calc-history">{st.session_state.history}&nbsp;</div>
    <div class="calc-result">{st.session_state.display}</div>
</div>
""", unsafe_allow_html=True)


# ── Button Renderer ────────────────────────────────────────
def btn(col, label, val, color="#3a3a3c"):
    with col:
        st.markdown(f"""
        <style>
        div[data-testid="stButton"]:has(button[title="{val}")) button {{
            background-color: {color} !important;
            color: #fff !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button(label, key=f"k_{val}_{label}", help=val):
            btn_click(val)


# ── Row 1 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**%**",   key="pct",  use_container_width=True): btn_click("PCT")
with c[1]:
    if st.button("**CE**",  key="ce",   use_container_width=True): btn_click("CE")
with c[2]:
    if st.button("**C**",   key="cl",   use_container_width=True): btn_click("C")
with c[3]:
    if st.button("**⌫**",   key="back", use_container_width=True): btn_click("DEL")

# ── Row 2 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**1/x**", key="inv",  use_container_width=True): btn_click("INV")
with c[1]:
    if st.button("**x²**",  key="sq",   use_container_width=True): btn_click("SQ")
with c[2]:
    if st.button("**√x**",  key="sqrt", use_container_width=True): btn_click("SQRT")
with c[3]:
    if st.button("**÷**",   key="div",  use_container_width=True): btn_click("/")

# ── Row 3 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**7**",   key="n7",   use_container_width=True): btn_click("7")
with c[1]:
    if st.button("**8**",   key="n8",   use_container_width=True): btn_click("8")
with c[2]:
    if st.button("**9**",   key="n9",   use_container_width=True): btn_click("9")
with c[3]:
    if st.button("**×**",   key="mul",  use_container_width=True): btn_click("*")

# ── Row 4 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**4**",   key="n4",   use_container_width=True): btn_click("4")
with c[1]:
    if st.button("**5**",   key="n5",   use_container_width=True): btn_click("5")
with c[2]:
    if st.button("**6**",   key="n6",   use_container_width=True): btn_click("6")
with c[3]:
    if st.button("**−**",   key="sub",  use_container_width=True): btn_click("-")

# ── Row 5 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**1**",   key="n1",   use_container_width=True): btn_click("1")
with c[1]:
    if st.button("**2**",   key="n2",   use_container_width=True): btn_click("2")
with c[2]:
    if st.button("**3**",   key="n3",   use_container_width=True): btn_click("3")
with c[3]:
    if st.button("**+**",   key="add",  use_container_width=True): btn_click("+")

# ── Row 6 ──────────────────────────────────────────────────
c = st.columns(4, gap="small")
with c[0]:
    if st.button("**+/-**", key="neg",  use_container_width=True): btn_click("NEG")
with c[1]:
    if st.button("**0**",   key="n0",   use_container_width=True): btn_click("0")
with c[2]:
    if st.button("**.**",   key="dot",  use_container_width=True): btn_click(".")
with c[3]:
    if st.button("**=**",   key="eq",   use_container_width=True): btn_click("=")
