# ============================================
# PROGRAM 8: Flask Web Calculator
# pip install flask
# Run: python app.py
# Open: http://localhost:5000
# ============================================

from flask import Flask, render_template, jsonify, request
import math

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data   = request.get_json()
    action = data.get("action")
    expr   = data.get("expr", "")

    try:
        if action == "eval":
            result = eval(expr, {"__builtins__": {}}, {"sqrt": math.sqrt, "pi": math.pi})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            result = round(float(result), 10)
            if result == int(result):
                result = int(result)
            return jsonify({"result": str(result), "error": False})

        elif action == "sqrt":
            num = float(expr)
            if num < 0:
                return jsonify({"result": "Invalid", "error": True})
            r = math.sqrt(num)
            r = int(r) if r == int(r) else round(r, 10)
            return jsonify({"result": str(r), "error": False})

        elif action == "square":
            r = float(expr) ** 2
            r = int(r) if r == int(r) else round(r, 10)
            return jsonify({"result": str(r), "error": False})

        elif action == "reciprocal":
            num = float(expr)
            if num == 0:
                return jsonify({"result": "Can't ÷ by 0", "error": True})
            r = round(1 / num, 10)
            return jsonify({"result": str(r), "error": False})

        elif action == "percent":
            r = float(expr) / 100
            return jsonify({"result": str(r), "error": False})

        elif action == "negate":
            r = float(expr) * -1
            r = int(r) if r == int(r) else r
            return jsonify({"result": str(r), "error": False})

    except ZeroDivisionError:
        return jsonify({"result": "Can't ÷ by 0", "error": True})
    except:
        return jsonify({"result": "Error", "error": True})

if __name__ == "__main__":
    print("\n  Calculator running at: http://localhost:5000\n")
    app.run(debug=False)
