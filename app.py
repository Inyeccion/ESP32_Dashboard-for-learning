from flask import Flask, render_template, request, redirect
import os
from mqtt_client import get_latest_data, publish_set_temperature, predict_temperature, model, scaler
import pandas as pd
import numpy as np

app = Flask(__name__)

# 全局变量存储目标温度
target_temperature = None

@app.route('/')
def index():
    global target_temperature
    temperature, humidity = get_latest_data()
    # 获取预测温度
    predicted_temp = None
    try:
        data = pd.read_csv("temperature_data.csv")
        if model is not None and scaler is not None and len(data) > 10:
            recent_data = data["temperature"].values[-10:]
            predicted = predict_temperature(model, scaler, np.array(recent_data))
            predicted_temp = round(float(predicted[0][0]), 2)
    except Exception as e:
        print("预测温度获取失败：", e)
    return render_template(
        'index.html',
        temperature=temperature,
        humidity=humidity,
        target_temperature=target_temperature,
        predicted_temp=predicted_temp
    )

@app.route('/set-temperature', methods=['POST'])
def set_temperature():
    global target_temperature
    target_temp = request.form.get('target_temperature')
    if target_temp:
        try:
            target_temperature = float(target_temp)  # 更新目标温度
            publish_set_temperature(target_temperature)
        except ValueError:
            print("无效温度输入")
    return redirect('/')
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
