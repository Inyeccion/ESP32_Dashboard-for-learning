from flask import Flask, render_template, request, redirect, jsonify
import os
from mqtt_client import get_latest_data, publish_set_temperature
import pandas as pd

app = Flask(__name__)

# 全局变量存储目标温度
target_temperature = None

@app.route('/')
def index():
    global target_temperature
    temperature, humidity, predicted_temp = get_latest_data()
    return render_template(   # 将初始化的四个值传递给模板
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
            target_temperature = float(target_temp)  
            publish_set_temperature(target_temperature)  # 更新目标温度
        except ValueError:
            print("无效温度输入")
    return redirect('/')
    
@app.route('/latest-data')    #实现实时更新  给前端提供json格式化后的最新数据
def latest_data():
    temperature, humidity, predicted_temperature = get_latest_data()
    if predicted_temperature is not None:
        predicted_temperature = float(predicted_temperature)
    return jsonify({
        "temperature": temperature,
        "humidity": humidity,
        "target_temperature": target_temperature,
        "predicted_temperature": predicted_temperature
    })

@app.route('/history-data')   # 实现历史数据显示  同样给前端提供json格式化后的历史数据
def history_data():
    try:
        df = pd.read_csv('temperature_data.csv')
        # 按时间降序排列
        df = df.sort_values(by='timestamp', ascending=False)
        # 只取最近100条数据（可根据需要调整）
        data = df.tail(100).to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify([])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
