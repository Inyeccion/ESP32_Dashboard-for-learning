# 项目简介
本项目为一个基于 Flask 的物联网（IoT）环境监控与控制平台。项目主要功能包括：

1. **实时数据展示**：前端页面可实时显示当前温度、湿度、目标温度和预测温度，数据每隔5秒自动刷新，确保用户获取最新环境信息。
2. **历史数据可视化**：通过 ECharts 动态绘制历史温度折线图，并以表格形式展示历史温度数据，便于用户分析环境变化趋势。
3. **目标温度设置**：用户可通过网页表单提交目标温度，后端接收并通过 MQTT 协议下发至设备，实现远程控制。
4. **预测温度展示**：系统可显示基于LSTM使用历史数据的温度预测结果，辅助用户决策。

项目关键逻辑流程如下：

- **数据采集与通信**：后端通过 MQTT 协议与传感器设备通信，采集温湿度数据并存储于本地。
- **数据接口设计**：Flask 提供 `/latest-data` 和 `/history-data` 等接口，分别用于获取最新环境数据和历史数据，供前端异步请求。
- **前端自动刷新**：前端 JavaScript 定时调用后端接口，动态更新页面上的实时数据、历史表格和折线图，实现无刷新体验。
- **目标温度控制**：用户提交目标温度后，后端通过 MQTT 向设备发布新目标，设备端据此调整运行状态。
- **数据可视化**：历史温度数据通过 ECharts 绘制为折线图，y 轴比例尺根据数据动态调整，提升可读性和美观性。

---

## 关键代码示例

**1. Flask 后端接口示例**

```python
@app.route('/latest-data')
def latest_data():
    temperature, humidity, predicted_temperature = get_latest_data()
    return jsonify({
        "temperature": temperature,
        "humidity": humidity,
        "target_temperature": target_temperature,
        "predicted_temperature": predicted_temperature
    })
```


**2. 前端自动刷新与数据渲染**
```python
function updateData() {
  fetch('/latest-data')
    .then(response => response.json())
    .then(data => {
      document.getElementById('current-temp').textContent = data.temperature;
      document.getElementById('current-humidity').textContent = data.humidity;
      document.getElementById('target-temp').textContent = data.target_temperature;
      document.getElementById('pred-temp').textContent =
        (data.predicted_temperature !== null && !isNaN(data.predicted_temperature))
          ? Number(data.predicted_temperature).toFixed(1)
          : '暂无预测';
    });
  fetch('/history-data')
    .then(response => response.json())
    .then(rows => {
      renderHistoryChart(rows); // 绘制折线图
    });
}
setInterval(updateData, 5000);
updateData();
```


**3. ECharts 折线图渲染**
```python
function renderHistoryChart(rows) {
  const times = rows.map(row => formatTime(row.timestamp));
  const temps = rows.map(row => row.temperature);
  let minTemp = Math.min(...temps);
  let maxTemp = Math.max(...temps);
  if (minTemp === maxTemp) {
    minTemp -= 1;
    maxTemp += 1;
  } else {
    minTemp = Math.floor(minTemp - 1);
    maxTemp = Math.ceil(maxTemp + 1);
  }
  const option = {
    xAxis: { type: 'category', data: times },
    yAxis: { type: 'value', min: minTemp, max: maxTemp },
    series: [{ data: temps, type: 'line', smooth: true }]
  };
  historyChart.setOption(option);
}
```



**整体架构实现了数据的实时采集、可视化展示与远程控制，适用于智能家居、实验室环境监控等物联网场景**