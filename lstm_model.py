import os
import csv
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

# 加载数据
def load_data(file_path, sequence_length=10):
    # 读取 CSV 文件并跳过表头
    data = pd.read_csv(file_path, skiprows=1, header=None, names=["timestamp", "temperature"])
    
    # 检查文件是否为空
    if data.empty:
        raise ValueError("temperature_data.csv 文件为空，请确保文件中有有效的温度数据。")
    
    # 提取温度列并转换为浮点数
    temperatures = data["temperature"].astype(float).values.reshape(-1, 1)

    # 数据归一化
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(temperatures)

    # 构建序列数据
    X, y = [], []
    for i in range(len(scaled_data) - sequence_length):
        X.append(scaled_data[i:i + sequence_length])
        y.append(scaled_data[i + sequence_length])
    return np.array(X), np.array(y), scaler

# 构建 LSTM 模型
def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model

# 训练模型
def train_model(file_path):
    X, y, scaler = load_data(file_path)
    model = build_model((X.shape[1], X.shape[2]))
    model.fit(X, y, epochs=20, batch_size=32)
    return model, scaler

# 预测未来温度
def predict_temperature(model, scaler, recent_data):
    recent_data = scaler.transform(recent_data.reshape(-1, 1))
    prediction = model.predict(recent_data.reshape(1, recent_data.shape[0], 1))
    return scaler.inverse_transform(prediction)