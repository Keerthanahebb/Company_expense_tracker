from fastapi import APIRouter
from app.ml.anomaly import detect_department_anomalies

router = APIRouter()

@router.get("/department-anomalies")
def department_anomalies():

    anomalies = detect_department_anomalies()

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies
    }