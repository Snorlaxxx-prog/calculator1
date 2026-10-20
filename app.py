
from flask import Flask, render_template, request
import math

app = Flask(__name__)


class Calculator:
    def __init__(self, numOne, numTwo=0):
        self._one = numOne
        self._two = numTwo

    def add(self):
        return self._one + self._two

    def minus(self):
        return self._one - self._two

    def times(self):
        return self._one * self._two

    def divide(self):
        if self._two == 0:
            raise ValueError("Cannot divide by zero.")
        return self._one / self._two

    def power(self):
        return self._one ** self._two

    def square(self):
        return self._one ** 2

    def square_root(self):
        if self._one < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return math.sqrt(self._one)

    def sine(self, mode):
        angle = self._one if mode == "RAD" else math.radians(self._one)
        return math.sin(angle)

    def cosine(self, mode):
        angle = self._one if mode == "RAD" else math.radians(self._one)
        return math.cos(angle)

    def tangent(self, mode):
        angle = self._one if mode == "RAD" else math.radians(self._one)

        if abs(math.cos(angle)) < 1e-12:
            raise ValueError("Tangent is undefined at this angle.")

        return math.tan(angle)

    def logarithm(self):
        if self._one <= 0:
            raise ValueError("Enter a number greater than zero.")
        return math.log10(self._one)

    def natural_log(self):
        if self._one <= 0:
            raise ValueError("Enter a number greater than zero.")
        return math.log(self._one)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    expression = ""
    numOne = ""
    numTwo = ""
    operation = "add"
    angleMode = "DEG"

    if request.method == "POST":
        expression = request.form.get("expression", "")
        numOne = request.form.get("numOne", "")
        numTwo = request.form.get("numTwo", "")
        operation = request.form.get("operation", "add")
        angleMode = request.form.get("angleMode", "DEG")

        try:
            first = float(numOne or 0)
            second = float(numTwo or 0)

            if angleMode not in ("DEG", "RAD"):
                raise ValueError("Invalid angle mode.")

            calc = Calculator(first, second)

            operations = {
                "add": calc.add,
                "minus": calc.minus,
                "times": calc.times,
                "divide": calc.divide,
                "power": calc.power,
                "square": calc.square,
                "sqrt": calc.square_root,
                "sin": lambda: calc.sine(angleMode),
                "cos": lambda: calc.cosine(angleMode),
                "tan": lambda: calc.tangent(angleMode),
                "log": calc.logarithm,
                "ln": calc.natural_log
            }

            if operation not in operations:
                raise ValueError("Invalid operation.")

            result = operations[operation]()

            if isinstance(result, complex) or not math.isfinite(result):
                raise ValueError("The result is too large or invalid.")

            result = f"{result:.10g}"

        except (ValueError, OverflowError) as e:
            error = str(e) or "Invalid calculation."

    return render_template(
        "calculator.html",
        result=result,
        error=error,
        expression=expression,
        numOne=numOne,
        numTwo=numTwo,
        operation=operation,
        angleMode=angleMode
    )


if __name__ == "__main__":
    app.run(debug=True)
