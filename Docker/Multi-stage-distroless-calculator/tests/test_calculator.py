from app.services.calculator_service import CalculatorService

def test_add():
    assert CalculatorService.add(2, 3) == 5

def test_sub():
    assert CalculatorService.sub(5, 3) == 2

def test_mul():
    assert CalculatorService.mul(2, 3) == 6

def test_div():
    assert CalculatorService.div(6, 3) == 2