
## HTML文件中增加的JavaScript代码的解释说明
1. function updateData() {...}
这是一个自定义函数，名字叫 updateData，它的作用是从服务器获取最新的数据并更新网页上的显示内容。
主要步骤如下：
a. fetch('/latest-data')
这行代码会向服务器的 /latest-data 路径发起一个 HTTP GET 请求。
你的 Flask 后端有一个对应的接口（@app.route('/latest-data')），会返回最新的温度、湿度和目标温度数据，格式为 JSON。
b. .then(response => response.json())
这一步把服务器返回的响应内容解析成 JSON 格式的数据对象。
c. .then(data => {...})
这里的 data 就是从服务器拿到的最新数据（比如 {temperature: 23.5, humidity: 60, target_temperature: 25}）。

下面三行代码分别用来更新页面上的温度、湿度和目标温度的显示内容：

document.querySelector('h3').textContent = ...
找到页面上第一个 <h3> 元素（显示当前温度），并把它的内容更新为最新温度。
document.querySelectorAll('h4')[0].textContent = ...
找到页面上第一个 <h4> 元素（显示当前湿度），并更新为最新湿度。
document.querySelectorAll('h4')[1].textContent = ...
找到页面上第二个 <h4> 元素（显示目标温度），并更新为最新目标温度。
2. setInterval(updateData, 5000);
这行代码的作用是每隔5秒（5000毫秒）自动执行一次 updateData() 函数。
这样页面就会不断地从服务器获取最新数据，实现“实时刷新”效果，无需手动刷新网页。
总结
这段代码让你的网页每5秒自动向服务器请求最新的温湿度和目标温度数据，并把数据显示在页面上，实现了实时监控的效果。
用户无需手动刷新页面，数据会自动更新。