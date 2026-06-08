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

    elif value == "⌫":
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

    elif value == "%":
        try:
            result = eval(expr) / 100
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            st.session_state.display    = str(result)
            st.session_state.expression = str(result)
        except:
            st.session_state.display    = "Error"
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


# ── Full UI using HTML Component ───────────────────────────
import streamlit.components.v1 as components

result = components.html(
    f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            background: #1c1c1e;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        .calculator {{
            background: #1c1c1e;
            border-radius: 24px;
            padding: 20px;
            width: 360px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }}

        .display {{
            background: #2c2c2e;
            border-radius: 16px;
            padding: 20px 18px 14px;
            text-align: right;
            margin-bottom: 16px;
            min-height: 110px;
        }}

        .history {{
            color: #888;
            font-size: 14px;
            min-height: 20px;
            margin-bottom: 6px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .result {{
            color: #fff;
            font-size: 50px;
            font-weight: 700;
            word-break: break-all;
            line-height: 1.1;
        }}

        .buttons {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }}

        button {{
            height: 72px;
            border: none;
            border-radius: 16px;
            font-size: 22px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            background: #3a3a3c;
            color: #fff;
        }}

        button:hover  {{ filter: brightness(1.25); }}
        button:active {{ transform: scale(0.93); }}

        .btn-special {{ background: #636366; font-size: 18px; }}
        .btn-operator {{ background: #FF9F0A; }}
        .btn-equals   {{ background: #0A84FF; }}
    </style>
    </head>
    <body>
    <div class="calculator">

        <div class="display">
            <div class="history">{st.session_state.history}&nbsp;</div>
            <div class="result">{st.session_state.display}</div>
        </div>

        <div class="buttons">
            <!-- Row 1 -->
            <button class="btn-special" onclick="sendVal('%')">%</button>
            <button class="btn-special" onclick="sendVal('CE')">CE</button>
            <button class="btn-special" onclick="sendVal('C')">C</button>
            <button class="btn-special" onclick="sendVal('⌫')">⌫</button>

            <!-- Row 2 -->
            <button class="btn-special" onclick="sendVal('1/x')">1/x</button>
            <button class="btn-special" onclick="sendVal('x²')">x²</button>
            <button class="btn-special" onclick="sendVal('√x')">√x</button>
            <button class="btn-operator" onclick="sendVal('/')">÷</button>

            <!-- Row 3 -->
            <button onclick="sendVal('7')">7</button>
            <button onclick="sendVal('8')">8</button>
            <button onclick="sendVal('9')">9</button>
            <button class="btn-operator" onclick="sendVal('*')">×</button>

            <!-- Row 4 -->
            <button onclick="sendVal('4')">4</button>
            <button onclick="sendVal('5')">5</button>
            <button onclick="sendVal('6')">6</button>
            <button class="btn-operator" onclick="sendVal('-')">−</button>

            <!-- Row 5 -->
            <button onclick="sendVal('1')">1</button>
            <button onclick="sendVal('2')">2</button>
            <button onclick="sendVal('3')">3</button>
            <button class="btn-operator" onclick="sendVal('+')">+</button>

            <!-- Row 6 -->
            <button class="btn-special" onclick="sendVal('+/-')">+/-</button>
            <button onclick="sendVal('0')">0</button>
            <button onclick="sendVal('.')">.</button>
            <button class="btn-equals" onclick="sendVal('=')">=</button>
        </div>
    </div>

    <script>
        function sendVal(val) {{
            window.parent.postMessage({{type: 'streamlit:setComponentValue', value: val}}, '*');
        }}
    </script>
    </body>
    </html>
    """,
    height=600,
)

# Process button click from HTML
if result is not None:
    btn_click(result)
    st.rerun()
