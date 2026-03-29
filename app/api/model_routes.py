from fastapi import APIRouter
from app.ml.model_train import train_model

router = APIRouter()

@router.post("/train-model")
def train():

    result = train_model()

    return {
        "message": "Model trained successfully",
        "model_version": result["version"],
        "accuracy": result["accuracy"]
    }