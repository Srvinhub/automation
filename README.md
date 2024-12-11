步骤 1：进入你的 GitHub 仓库
打开你的 GitHub 仓库页面。
点击页面右上角的 Settings 按钮。
步骤 2：访问 Secrets 页面
在 Settings 页面左侧，找到并点击 Secrets and variables。
点击 Actions 进入管理 GitHub Actions 密钥的页面。
步骤 3：添加新的 Secret
在 Secrets 页面，点击 New repository secret 按钮。
在 Name 输入框中，填写 SSH_INFO，这是你在配置中所需的密钥名称。
在 Value 输入框中，填写包含 SSH 连接信息的 JSON 字符串。

[
  {"hostname": "s5.serv00.com", "username": "user", "password": "password"}
]

添加 Telegram Bot Token
Name: TELEGRAM_BOT_TOKEN

添加 Telegram Chat ID
Name: TELEGRAM_CHAT_ID

添加推送渠道（例如 Mail 或 Telegram）
Name: PUSH
Value: 通知的推送渠道。示例：mail 或 telegram

添加邮件地址（如果推送渠道为 mail）
Name: MAIL
Value: 接收通知的邮箱地址。例如：mail@mail.com

步骤 4：保存 Secret
在填写完每个 Secret 的名称和值后，点击 Add secret 按钮保存。
