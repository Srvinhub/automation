import os
import json
import paramiko
import requests
from datetime import datetime, timezone, timedelta

def ssh_execute_commands(hosts_info, command):
    """
    通过SSH连接多个主机并执行指定命令
    :param hosts_info: 包含主机信息的列表 [{hostname, username, password}]
    :param command: 要执行的命令
    :return: 执行结果的用户名和主机名列表
    """
    users = []
    hostnames = []
    
    for host_info in hosts_info:
        hostname = host_info.get('hostname')
        username = host_info.get('username')
        password = host_info.get('password')

        if not (hostname and username and password):
            print(f"缺少主机信息，跳过：{host_info}")
            continue

        try:
            with paramiko.SSHClient() as ssh:
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=hostname, port=22, username=username, password=password)
                stdin, stdout, stderr = ssh.exec_command(command)
                user = stdout.read().decode().strip()
                users.append(user)
                hostnames.append(hostname)
        except paramiko.SSHException as e:
            print(f"无法连接到主机 {hostname}，错误：{e}")
        except Exception as e:
            print(f"执行命令时发生未知错误：{e}")

    return users, hostnames

def get_public_ip():
    """获取当前设备的公网 IP 地址"""
    try:
        response = requests.get('https://checkip.amazonaws.com', timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.RequestException as e:
        print(f"获取公网IP失败：{e}")
        return "未知IP"

def get_telegram_menu():
    """获取Telegram菜单配置"""
    try:
        response = requests.get('https://example.com/telegram/menu', timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"获取Telegram菜单失败：{e}")
        return []

def format_content(users, hostnames, user_num, time, login_ip):
    """格式化消息内容"""
    content = "SSH服务器登录信息：\n"
    for user, hostname in zip(users, hostnames):
        content += f"用户名：{user}，服务器：{hostname}\n"
    content += f"本次登录用户共： {user_num} 个\n登录时间：{time}\n登录IP：{login_ip}"
    return content

def push_to_email(content):
    """推送内容到邮箱"""
    mail_url = os.getenv('MAIL_PUSH_URL')
    email = os.getenv('MAIL')
    if not (mail_url and email):
        print("邮箱推送配置缺失")
        return

    data = {"body": content, "email": email}
    try:
        response = requests.post(mail_url, json=data, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get('code') == 200:
            print("邮件推送成功")
        else:
            print(f"邮件推送失败，错误代码：{response_data.get('code')}")
    except requests.RequestException as e:
        print(f"邮件推送失败：{e}")

def push_to_telegram(content, menu):
    """推送内容到Telegram"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not (bot_token and chat_id):
        print("Telegram推送配置缺失")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': content,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps({"inline_keyboard": menu})
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("Telegram推送成功")
    except requests.RequestException as e:
        print(f"Telegram推送失败：{e}")

if __name__ == "__main__":
    # 获取主机信息
    ssh_info_str = os.getenv('SSH_INFO', '[]')
    hosts_info = json.loads(ssh_info_str)

    # 执行SSH命令
    command = 'whoami'
    user_list, hostname_list = ssh_execute_commands(hosts_info, command)

    # 格式化推送内容
    user_num = len(user_list)
    beijing_timezone = timezone(timedelta(hours=8))
    time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
    login_ip = get_public_ip()
    menu = get_telegram_menu()
    content = format_content(user_list, hostname_list, user_num, time, login_ip)

    # 推送消息
    push_method = os.getenv('PUSH')
    if push_method == "mail":
        push_to_email(content)
    elif push_method == "telegram":
        push_to_telegram(content, menu)
    else:
        print("未指定正确的推送方式")
