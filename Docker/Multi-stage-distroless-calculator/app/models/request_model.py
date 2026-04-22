from pydantic import BaseModel

class CalculationRequest(BaseModel):
    operation: str
    a: float
    b: float