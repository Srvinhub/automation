# SSH Login Workflow

## 配置 Secrets

进入仓库页面 > "Settings" > "Secrets" 中添加以下 Secrets：

- **SSH_INFO**：包含 SSH 连接信息的 JSON 字符串。例如：
  ```json
  [
    {"hostname": "s10.serv00.com", "username": "user", "password": "password"}
  ]
  ```

- **TELEGRAM_BOT_TOKEN**：您的 Telegram Bot API Token。
- **TELEGRAM_CHAT_ID**：您的 Telegram Chat ID。
- **PUSH**：推送渠道，值为 `mail` 或者 `telegram`。例如：`mail`
- **MAIL**：接收通知的邮箱。例如：`mail@mail.com`

## 测试运行

1. 在 GitHub 仓库的 **"Actions"** 选项卡中，手动触发运行一次工作流程。
   - 进入 **"Actions"** 页面。
   - 点击 **"Run SSH Login"**。
   - 选择 **"Run workflow"** > **"Run workflow"**。

2. 检查运行结果。
   - 如果没有报错，说明运行成功。
   - 点击运行记录列表中的某一项可以查看运行的详细情况。

## 定时自动运行

此工作流默认每周的周一 **北京时间 0 点** 运行。

### 调整运行时间

您可以根据需要修改调度时间：
```yaml
- cron: '0 16 * * 0'  # 每周的周一 北京时间 0 点运行
```

