from flask import Flask, render_template, request, redirect
import os
from mqtt_client import get_latest_data, publish_set_temperature

app = Flask(__name__)

# 全局变量存储目标温度
target_temperature = None

@app.route('/')
def index():
    global target_temperature
    temperature, humidity = get_latest_data()
    return render_template('index.html', temperature=temperature, humidity=humidity, target_temperature=target_temperature)

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
