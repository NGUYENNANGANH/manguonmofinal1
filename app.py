# from fastapi import FastAPI
# from pydantic import BaseModel
# import pandas as pd
# import pickle
# from statsmodels.tsa.arima.model import ARIMA

# app = FastAPI()

# class CovidData(BaseModel):
#     current_cases: int
#     steps: int

# # Hàm để tải mô hình đã huấn luyện từ tệp
# def load_model():
#     try:
#         with open("model.pkl", "rb") as f:
#             model_fit = pickle.load(f)
#     except FileNotFoundError:
#         model_fit = None
#     return model_fit

# # Nếu mô hình chưa được tải, thông báo lỗi
# model_fit = load_model()
# if model_fit is None:
#     raise Exception("Mô hình không tồn tại. Hãy huấn luyện lại mô hình và lưu vào tệp 'covid_model.pkl'.")

# @app.post("/predict/")
# def predict_trend(data: CovidData):
#     trend, predicted_cases = predict_trend_logic(data.current_cases, data.steps)
#     return {"trend": trend, "predicted_cases": predicted_cases}

# def predict_trend_logic(current_cases, steps):
#     # Dự đoán số ca trong `steps` ngày tiếp theo
#     forecast = model_fit.forecast(steps=steps)
#     predicted_cases = forecast[-1]

#     # So sánh với số ca hiện tại
#     if predicted_cases > current_cases:
#         trend = "Số ca dự đoán tăng"
#     elif predicted_cases < current_cases:
#         trend = "Số ca dự đoán giảm"
#     else:
#         trend = "Số ca dự đoán không đổi"

#     return trend, predicted_cases





from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from statsmodels.tsa.arima.model import ARIMA

app = FastAPI()

class CovidData(BaseModel):
    current_cases: int
    steps: int

# Hàm để tải mô hình đã huấn luyện từ tệp
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            model_fit = pickle.load(f)
    except FileNotFoundError:
        return None
    return model_fit

# Kiểm tra xem mô hình đã được tải chưa
model_fit = load_model()

@app.get("/model_status/")
def model_status():
    if model_fit is None:
        return {"status": "Model not loaded", "message": "Please train and save the model first."}
    return {"status": "Model loaded", "message": "Model is ready for prediction."}

# Hàm dự đoán xu hướng
@app.post("/predict/")
def predict_trend(data: CovidData):
    if model_fit is None:
        return {"error": "Model is not loaded. Please load or train the model."}
    trend, predicted_cases = predict_trend_logic(data.current_cases, data.steps)
    return {"trend": trend, "predicted_cases": predicted_cases}

def predict_trend_logic(current_cases, steps):
    # Dự đoán số ca trong `steps` ngày tiếp theo
    forecast = model_fit.forecast(steps=steps)
    predicted_cases = forecast[-1]

    # So sánh với số ca hiện tại
    if predicted_cases > current_cases:
        trend = "Số ca dự đoán tăng"
    elif predicted_cases < current_cases:
        trend = "Số ca dự đoán giảm"
    else:
        trend = "Số ca dự đoán không đổi"

    return trend, predicted_cases
