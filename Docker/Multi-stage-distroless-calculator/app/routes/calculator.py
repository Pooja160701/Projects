from fastapi import APIRouter, HTTPException
from app.models.request_model import CalculationRequest
from app.services.calculator_service import CalculatorService
from app.utils.logger import logger

router = APIRouter()

@router.post("/calculate")
def calculate(request: CalculationRequest):
    logger.info(f"Request received: {request}")

    try:
        operations = {
            "add": CalculatorService.add,
            "sub": CalculatorService.sub,
            "mul": CalculatorService.mul,
            "div": CalculatorService.div,
        }

        if request.operation not in operations:
            logger.warning("Invalid operation attempted")
            raise HTTPException(status_code=400, detail="Invalid operation")

        result = operations[request.operation](request.a, request.b)

        logger.info(f"Calculation result: {result}")

        return {
            "operation": request.operation,
            "a": request.a,
            "b": request.b,
            "result": result
        }

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))