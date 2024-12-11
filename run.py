import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取环境变量
SSH_INFO = os.getenv('SSH_INFO', '[]')
PUSH = os.getenv('PUSH', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MAIL = os.getenv('MAIL')

# 获取当前时间（北京时间）
def get_beijing_time():
    beijing_timezone = timezone(timedelta(hours=8))
    return datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')

# 批量 SSH 登录并执行命令
def ssh_multiple_connections(hosts_info, command):
    users = []
    hostnames = []
    for host_info in hosts_info:
        hostname = host_info['hostname']
        username = host_info['username']
        password = host_info['password']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            user = stdout.read().decode().strip()
            users.append(user)
            hostnames.append(hostname)
            ssh.close()
        except Exception as e:
            print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
    return users, hostnames

# 获取当前公共 IP
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        return response.json().get('ip', '未知')
    except requests.RequestException as e:
        print(f"获取公共 IP 失败: {e}")
        return "未知"

# 邮件推送
def mail_push(url, content):
    if not MAIL:
        print("邮件地址未配置，无法发送邮件")
        return
    data = {
        "body": content,
        "email": MAIL
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        response_data = response.json()
        if response_data.get('code') == 200:
            print("邮件推送成功")
        else:
            print(f"邮件推送失败，错误代码：{response_data.get('code')}")
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"邮件推送失败: {e}")

# Telegram 推送
def telegram_push(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram 推送信息未配置")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Telegram 推送成功")
    except requests.RequestException as e:
        print(f"Telegram 推送失败: {e}")

# 主逻辑
def main():
    # 解析 SSH 信息
    try:
        hosts_info = json.loads(SSH_INFO)
    except json.JSONDecodeError:
        print("SSH_INFO 格式错误，请检查环境变量")
        return

    # 执行 SSH 命令
    command = 'whoami'
    user_list, hostname_list = ssh_multiple_connections(hosts_info, command)
    user_num = len(user_list)

    # 生成推送内容
    content = "SSH服务器登录信息：\n"
    for user, hostname in zip(user_list, hostname_list):
        content += f"用户名：{user}，服务器：{hostname}\n"
    content += f"本次登录用户共： {user_num} 个\n"
    content += f"登录时间：{get_beijing_time()}\n"
    content += f"登录IP：{get_public_ip()}"

    # 推送消息
    if PUSH == "mail":
        mail_push('https://your-mail-api-url.com', content)
    elif PUSH == "telegram":
        telegram_push(content)
    else:
        print("推送失败，PUSH 参数设置错误")

if __name__ == "__main__":
    main()