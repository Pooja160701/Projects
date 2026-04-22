class CalculatorService:

    @staticmethod
    def add(a: float, b: float):
        return a + b

    @staticmethod
    def sub(a: float, b: float):
        return a - b

    @staticmethod
    def mul(a: float, b: float):
        return a * b

    @staticmethod
    def div(a: float, b: float):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b