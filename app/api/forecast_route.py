from fastapi import APIRouter
from app.ml.forecasting import generate_forecast

router = APIRouter()

@router.get("/forecast/{department_id}")
def forecast(department_id: int):

    forecast = generate_forecast(department_id)

    return {
        "department_id": department_id,
        "forecast": forecast
    }