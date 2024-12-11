import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# SSH 批量连接并执行命令
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

# 获取 SSH 连接信息
ssh_info_str = os.getenv('SSH_INFO', '[]')
hosts_info = json.loads(ssh_info_str)

# 执行的命令
command = 'whoami'
user_list, hostname_list = ssh_multiple_connections(hosts_info, command)
user_num = len(user_list)

# 构建推送内容
content = "SSH服务器登录信息：\n"
for user, hostname in zip(user_list, hostname_list):
    content += f"用户名：{user}，服务器：{hostname}\n"
beijing_timezone = timezone(timedelta(hours=8))
time = datetime.now(beijing_timezone).strftime('%Y-%m-%d %H:%M:%S')
menu = requests.get('https://api.zzzwb.com/v1?get=tg').json()  # 可自定义API获取菜单数据
loginip = requests.get('https://api.ipify.org?format=json').json()['ip']
content += f"本次登录用户共： {user_num} 个\n登录时间：{time}\n登录IP：{loginip}"

push = os.getenv('PUSH')

# 使用 SendGrid 发送邮件推送
def mail_push():
    content = "你的邮件内容"  # 此处替换为具体的邮件内容
    mail = Mail(
        from_email=Email("your-email@example.com"),  # 替换为你的发件人邮箱
        to_emails=To(os.getenv('MAIL')),  # 目标邮箱
        subject="SSH 登录通知",
        plain_text_content=Content("text/plain", content)
    )
    
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.getenv('SENDGRID_API_KEY'))  # 使用 SendGrid API 密钥
        response = sg.send(mail)
        if response.status_code == 202:
            print("邮件推送成功")
        else:
            print(f"邮件推送失败，错误代码：{response.status_code}")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")

# Telegram 推送
def telegram_push(message):
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
    payload = {
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'text': message,
        'parse_mode': 'HTML',
        'reply_markup': json.dumps({
            "inline_keyboard": menu,
            "one_time_keyboard": True
         })
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        print(f"发送消息到Telegram失败: {response.text}")

# 判断推送方式
if push == "mail":
    mail_push()
elif push == "telegram":
    telegram_push(content)
else:
    print("推送失败，推送参数设置错误")