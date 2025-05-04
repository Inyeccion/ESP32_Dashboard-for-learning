1. 确保代码已上传到 GitHub
Render 需要从 GitHub 仓库中拉取代码。请确保你的代码已经推送到 GitHub，并且仓库是公开的或你已授权 Render 访问私有仓库。
2. 登录 Render 并创建新服务
登录 Render。
点击 "New +" 按钮，选择 "Web Service"。
连接你的 GitHub 账户，并选择你的代码仓库。
3. 配置 Render 服务
在配置页面中：

Name: 输入服务的名称，例如 iot-dashboard。
Environment: 选择 Python。
Build Command: 使用以下命令安装依赖：
```
pip install -r requirements.txt
```
Start Command: 使用以下命令启动 Flask 应用：
```
python app.py
```
Port: Render 会自动检测 Flask 默认运行的端口（5000）。无需额外配置。
