import paho.mqtt.client as mqtt
import json

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
    global latest_temperature, latest_humidity
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        # Todo 1 开始: 更新到到全局变量latest_temperature, latest_humidity
        # code here
        latest_temperature = data["temperature"]
        latest_humidity = data["humidity"]
        print(f"收到消息:{data}")
        # Todo 1 结束
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
        client.publish(MQTT_SET_TOPIC, temp)
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
