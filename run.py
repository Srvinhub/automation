import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量（如果存在）
load_dotenv()

# 获取环境变量
ssh_info_str = os.getenv('SSH_INFO', '[]')  # 默认值为空列表
push_method = os.getenv('PUSH', '').lower()  # 推送方式
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
mail = os.getenv('MAIL', '')

# SSH 多连接函数
def ssh_multiple_connections(hosts_info, command):
    users = []
    hostnames = []
    for host_info in hosts_info:
        hostname = host_info.get('hostname')
        username = host_info.get('username')
        password = host_info.get('password')

        try:
            # 配置并建立 SSH 连接
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)

            # 执行命令
            stdin, stdout, stderr = ssh.exec_command(command)
            user = stdout.read().decode().strip()
            users.append(user)
            hostnames.append(hostname)
            ssh.close()
        except Exception as e:
            print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
    return users, hostnames

# 解析 SSH 信息
try:
    hosts_info = json.loads(ssh_info_str)
except json.JSONDecodeError:
    print("SSH_INFO 格式错误，请检查 JSON 配置")
    hosts_info = []

# 执行 SSH 命令
command = 'whoami'
user_list, hostname_list = ssh_multiple_connections(hosts_info, command)

# 整理消息内容
user_num = len(user_list)
content = "SSH服务器登录信息：\n"
for user, hostname in zip(user_list, hostname_list):
    content += f"用户名：{user}，服务器：{hostname}\n"

# 获取时间和 IP 信息
beijing_timezone = timezone(timedelta(hours=8))
current_time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')

try:
    login_ip = requests.get('https://api.ipify.org?format=json', timeout=5).json().get('ip', '未知')
except requests.RequestException:
    login_ip = "无法获取"

content += f"本次登录用户共： {user_num} 个\n登录时间：{current_time}\n登录IP：{login_ip}"

# 推送邮件通知
def mail_push():
    if not mail:
        print("未配置接收邮件地址，跳过邮件推送")
        return

    url = "https://your-mail-api.example.com/send"  # 替换为实际邮件 API
    data = {
        "body": content,
        "email": mail
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        response_data = response.json()
        if response_data.get('code') == 200:
            print("邮件推送成功")
        else:
            print(f"邮件推送失败，错误代码：{response_data.get('code', '未知')}")
    except Exception as e:
        print(f"邮件推送失败: {str(e)}")

# 推送 Telegram 通知
def telegram_push():
    if not telegram_bot_token or not telegram_chat_id:
        print("未配置 Telegram Bot Token 或 Chat ID，跳过 Telegram 推送")
        return

    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        'chat_id': telegram_chat_id,
        'text': content,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("Telegram 推送成功")
        else:
            print(f"Telegram 推送失败: {response.text}")
    except Exception as e:
        print(f"Telegram 推送失败: {str(e)}")

# 推送逻辑
if push_method == "mail":
    mail_push()
elif push_method == "telegram":
    telegram_push()
else:
    print("推送失败，请检查 PUSH 环境变量是否正确设置")