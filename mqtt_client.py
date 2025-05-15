import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime
from flask import Flask, jsonify
from lstm_model import train_model, predict_temperature
import numpy as np
import os
import pandas as pd

# 每次启动时清空 temperature_data.csv 并写入表头
with open("temperature_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "temperature"])  # 添加表头

# 延迟训练模型
model, scaler = None, None
if os.path.exists("temperature_data.csv") and os.path.getsize("temperature_data.csv") > 0:
    data = pd.read_csv("temperature_data.csv")
    if len(data) > 10:  # 假设需要至少 10 条数据
        model, scaler = train_model("temperature_data.csv")
        print("LSTM 模型已训练完成")
    else:
        print("数据不足，等待更多数据后再训练模型...")
else:
    print("temperature_data.csv 文件为空或不存在，等待数据积累...")

# MQTT 参数
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "sc104/9013/get_temperature"
MQTT_SET_TOPIC = "sc104/9013/set_temperature"

# 全局变量保存最新温湿度数据
latest_temperature = None
latest_humidity = None

# 当连接成功时的回调
def on_connect(client, userdata, flags, rc):
    print("已连接到 MQTT Broker，返回码：" + str(rc))
    client.subscribe(MQTT_TOPIC)
    print(f"已订阅主题：{MQTT_TOPIC}")

# 当接收到消息时的回调
def on_message(client, userdata, msg):
    global latest_temperature, latest_humidity, model, scaler
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        latest_temperature = data["temperature"]
        latest_humidity = data["humidity"]
        print(f"收到消息:{data}")

        # 将温度数据存储到 CSV 文件
        with open("temperature_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), latest_temperature])

        # 检查数据量是否足够进行预测
        data = pd.read_csv("temperature_data.csv")
        if len(data) > 10:  # 假设需要至少 10 条数据
            # 如果模型未训练或需要更新，则重新训练
            if model is None or len(data) % 10 == 0:  # 每 10 条数据更新一次模型
                model, scaler = train_model("temperature_data.csv")
                print("LSTM 模型已更新")

            # 使用最新数据进行预测
            recent_data = data["temperature"].values[-10:]  # 获取最近 10 条数据
            predicted_temp = predict_temperature(model, scaler, np.array(recent_data))
            print(f"预测的未来温度: {predicted_temp[0][0]}")

    except Exception as e:
        print("解析错误:", e)
        print("消息内容:", msg.payload)

# Flask 可调用的接口：获取最新数据
def get_latest_data():
    return latest_temperature, latest_humidity


def publish_set_temperature(temp):
    if client.is_connected():
        # Todo 2 开始：将目标温度转换为 JSON 格式，并发布到指定主题MQTT_SET_TOPIC
        pass
        # code here
        data = json.dumps({"target_temperature": temp})
        client.publish(MQTT_SET_TOPIC, data)
        print(f"发布目标温度: {temp}")
        
        # Todo 2 结束
    else:
        print("MQTT 未连接，无法发布设定温度")

# 创建并启动 MQTT 客户端
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()  # 使用非阻塞模式以便与 Flask 共存

print(f"MQTT 客户端已启动，等待来自 {MQTT_TOPIC} 的消息...")

# Flask 应用
app = Flask(__name__)

@app.route("/predict", methods=["GET"])
def predict():
    global model, scaler
    data = pd.read_csv("temperature_data.csv")
    if len(data) > 10:
        recent_data = data["temperature"].values[-10:]  # 获取最近 10 条数据
        predicted_temp = predict_temperature(model, scaler, np.array(recent_data))
        return jsonify({"predicted_temperature": predicted_temp[0][0]})
    else:
        return jsonify({"error": "数据不足，无法进行预测"})

# 导出模型、scaler和预测函数
__all__ = ['get_latest_data', 'publish_set_temperature', 'predict_temperature', 'model', 'scaler']

if __name__ == "__main__":
    app.run(debug=True)
