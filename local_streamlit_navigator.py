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
    st.title("Local Streamlit Navigator")

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
            st.info("Streamlit程序已在运行")

    # 保存配置文件
    save_config(config)

    # 显示所有streamlit应用程序的链接
    st.header("Streamlit 程序列表")
    for app_folder, app_info in config.items():
        st.write(f"**{app_folder}**: **{app_info['url']}**")

if __name__ == "__main__":
    main()
