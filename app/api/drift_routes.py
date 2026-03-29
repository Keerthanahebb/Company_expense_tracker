from fastapi import APIRouter
from app.ml.drift import calculate_drift

router = APIRouter()

@router.get("/drift-status")
def drift_status():

    drift_score = calculate_drift()

    return {
        "drift_score": drift_score
    }