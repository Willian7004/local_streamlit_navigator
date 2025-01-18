### user:

使用streamlit写一个程序，实现以下功能：

1.扫描当前文件夹的子文件夹中所有streamlit_app.py文件，切换到相应文件夹后在随机端口启动这些程序并避免端口冲突。

2.创建一个json文件记录上一步启动程序的地址（使用局域网地址）和对应文件夹名称，在刷新时避免重新启动程序。

3.在页面上显示第1步的程序中的文件夹名称以及指向对应的局域网地址的链接。

### addistant:

要实现这个功能，我们可以使用Python编写一个Streamlit应用程序。这个应用程序将扫描当前文件夹的子文件夹，查找所有的`streamlit_app.py`文件，并在随机端口上启动这些应用程序。同时，它会记录这些应用程序的地址和对应的文件夹名称，并在页面上显示这些信息。

以下是实现这个功能的代码：

```python
import os
import subprocess
import json
import socket
import random
import streamlit as st

# 配置文件路径
CONFIG_FILE = "streamlit_apps_config.json"

def get_local_ip():
    """获取本地局域网的IP地址"""
    try:
        # 创建一个UDP套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到Google的DNS服务器
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        st.error(f"无法获取本地IP地址: {e}")
        return "127.0.0.1"

def find_streamlit_apps(base_dir):
    """查找所有子文件夹中的streamlit_app.py文件"""
    streamlit_apps = []
    for root, dirs, files in os.walk(base_dir):
        if "streamlit_app.py" in files:
            streamlit_apps.append(root)
    return streamlit_apps

def start_streamlit_app(folder, port):
    """在指定端口启动streamlit应用程序"""
    try:
        # 切换到对应的文件夹
        os.chdir(folder)
        # 启动streamlit应用程序
        process = subprocess.Popen(["streamlit", "run", "streamlit_app.py", "--server.port", str(port)])
        return process
    except Exception as e:
        st.error(f"启动 {folder} 中的streamlit应用程序失败: {e}")
        return None

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def main():
    st.title("Streamlit 应用程序管理器")

    # 获取本地IP地址
    local_ip = get_local_ip()

    # 加载配置文件
    config = load_config()

    # 查找所有streamlit_app.py文件
    base_dir = os.getcwd()
    streamlit_apps = find_streamlit_apps(base_dir)

    # 启动或恢复streamlit应用程序
    for app_folder in streamlit_apps:
        if app_folder not in config:
            # 生成一个随机端口
            port = random.randint(8501, 9000)
            # 启动streamlit应用程序
            process = start_streamlit_app(app_folder, port)
            if process:
                # 记录应用程序的地址和端口
                config[app_folder] = {
                    "url": f"http://{local_ip}:{port}",
                    "port": port,
                    "process_id": process.pid
                }
        else:
            # 如果应用程序已经启动，直接使用配置中的信息
            st.info(f"{app_folder} 中的streamlit应用程序已经在运行: {config[app_folder]['url']}")

    # 保存配置文件
    save_config(config)

    # 显示所有streamlit应用程序的链接
    st.header("Streamlit 应用程序列表")
    for app_folder, app_info in config.items():
        st.write(f"**{app_folder}**: [打开应用程序]({app_info['url']})")

if __name__ == "__main__":
    main()
```

### 代码说明：

1. **获取本地IP地址**：`get_local_ip()` 函数用于获取本地局域网的IP地址，以便生成应用程序的访问链接。

2. **查找streamlit_app.py文件**：`find_streamlit_apps()` 函数会递归扫描当前文件夹及其子文件夹，查找所有包含`streamlit_app.py`文件的文件夹。

3. **启动streamlit应用程序**：`start_streamlit_app()` 函数会在指定的端口上启动`streamlit_app.py`文件。它会切换到对应的文件夹，并使用`subprocess.Popen`启动Streamlit应用程序。

4. **加载和保存配置**：`load_config()` 和 `save_config()` 函数用于加载和保存配置文件。配置文件记录了每个应用程序的访问地址、端口和进程ID。

5. **主程序**：`main()` 函数是Streamlit应用程序的入口。它会查找所有`streamlit_app.py`文件，启动或恢复这些应用程序，并在页面上显示它们的访问链接。

### 使用方法：

1. 将上述代码保存为`manager_app.py`。
2. 在终端中运行以下命令启动管理器应用程序：
   ```bash
   streamlit run manager_app.py
   ```
3. 打开浏览器，访问管理器应用程序的页面。你将看到所有子文件夹中的`streamlit_app.py`应用程序的链接。

### 注意事项：

- 确保所有子文件夹中的`streamlit_app.py`文件都可以独立运行。
- 如果端口冲突，可以调整`random.randint(8501, 9000)`的范围，选择一个更大的端口范围。
- 如果需要停止某个应用程序，可以手动终止对应的进程。

这个程序可以帮助你管理和启动多个Streamlit应用程序，并在一个统一的界面中访问它们。

