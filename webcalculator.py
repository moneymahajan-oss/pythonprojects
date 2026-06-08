import streamlit as st

st.set_page_config(
    page_title="Calculator",
    page_icon="🧮",
    layout="centered"
)

# ── Session State ──────────────────────────────────────────
defaults = {"expression": "", "display": "0", "history": "", "clicked": ""}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    elif value == "PCT":
        try:
            result = eval(expr) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display = "Error"
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

# ── Handle URL param click ─────────────────────────────────
params = st.query_params
if "v" in params:
    val = params["v"]
    btn_click(val)
    st.query_params.clear()
    st.rerun()

# ── Page Style ─────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    max-width: 380px !important;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
}
.stApp { background-color: #1c1c1e !important; }
</style>
""", unsafe_allow_html=True)

# ── Render Full Calculator as HTML ─────────────────────────
base_url = "?v="

html = f"""
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
.calc {{ width:100%; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }}

.display {{
    background:#2c2c2e;
    border-radius:16px;
    padding:20px 18px 14px;
    text-align:right;
    margin-bottom:14px;
    min-height:105px;
}}
.history {{
    color:#888;
    font-size:14px;
    min-height:20px;
    margin-bottom:4px;
    overflow:hidden;
    white-space:nowrap;
    text-overflow:ellipsis;
}}
.result {{
    color:#fff;
    font-size:50px;
    font-weight:700;
    word-break:break-all;
    line-height:1.1;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:10px;
}}

.btn {{
    display:block;
    height:70px;
    border-radius:14px;
    border:none;
    font-size:22px;
    font-weight:600;
    color:#fff;
    text-align:center;
    line-height:70px;
    text-decoration:none;
    cursor:pointer;
    background:#3a3a3c;
    transition: filter 0.12s, transform 0.1s;
    -webkit-tap-highlight-color: transparent;
}}
.btn:hover  {{ filter:brightness(1.3); color:#fff; text-decoration:none; }}
.btn:active {{ transform:scale(0.93); color:#fff; }}

.sp {{ background:#636366; font-size:18px; }}
.op {{ background:#FF9F0A; }}
.eq {{ background:#0A84FF; }}
</style>

<div class="calc">
  <div class="display">
    <div class="history">{st.session_state.history}&nbsp;</div>
    <div class="result">{st.session_state.display}</div>
  </div>

  <div class="grid">
    <a class="btn sp" href="{base_url}PCT">%</a>
    <a class="btn sp" href="{base_url}CE">CE</a>
    <a class="btn sp" href="{base_url}C">C</a>
    <a class="btn sp" href="{base_url}DEL">⌫</a>

    <a class="btn sp" href="{base_url}INV">1/x</a>
    <a class="btn sp" href="{base_url}SQ">x²</a>
    <a class="btn sp" href="{base_url}SQRT">√x</a>
    <a class="btn op" href="{base_url}/">÷</a>

    <a class="btn"    href="{base_url}7">7</a>
    <a class="btn"    href="{base_url}8">8</a>
    <a class="btn"    href="{base_url}9">9</a>
    <a class="btn op" href="{base_url}*">×</a>

    <a class="btn"    href="{base_url}4">4</a>
    <a class="btn"    href="{base_url}5">5</a>
    <a class="btn"    href="{base_url}6">6</a>
    <a class="btn op" href="{base_url}-">−</a>

    <a class="btn"    href="{base_url}1">1</a>
    <a class="btn"    href="{base_url}2">2</a>
    <a class="btn"    href="{base_url}3">3</a>
    <a class="btn op" href="{base_url}%2B">+</a>

    <a class="btn sp" href="{base_url}NEG">+/-</a>
    <a class="btn"    href="{base_url}0">0</a>
    <a class="btn"    href="{base_url}.">.</a>
    <a class="btn eq" href="{base_url}EQ">=</a>
  </div>
</div>
"""

st.html(html)
