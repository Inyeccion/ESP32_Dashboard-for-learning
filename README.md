# IoT控制台
## 功能
- 监控环境温度
- 监控环境湿度
- 设置目标温度

## 补全代码
- 完成代码mqtt_client.py中的Todo部分
```python
# 当接收到消息时的回调
def on_message(client, userdata, msg):
    global latest_temperature, latest_humidity
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        # Todo 1 开始: 更新到到全局变量latest_temperature, latest_humidity
        # code here
        # Todo 1 结束
    except Exception as e:
        print("解析错误:", e)
        print("消息内容:", msg.payload)
```

```python
def publish_set_temperature(temp):
    if client.is_connected():
        # Todo 2 开始：将目标温度转换为 JSON 格式，并发布到指定主题MQTT_SET_TOPIC
        pass
        # code here
        # Todo 2 结束
    else:
        print("MQTT 未连接，无法发布设定温度")
```


## 运行
```bash
python app.py
```