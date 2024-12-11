
### 配置Secrets

- 进入仓库页面>“Settings” > “Secrets”中添加以下Secrets：

- `SSH_INFO`：包含SSH连接信息的JSON字符串。以下是示例

  ```json
  [
    {"hostname": "s5.serv00.com", "username": "user", "password": "password"}
  ]
  ```
- TELEGRAM_BOT_TOKEN：您的 Telegram Bot API Token
- TELEGRAM_CHAT_ID：您的 Telegram Chat ID
- PUSH：推送渠道值为`mail`或者`telegram`。示例：`mail`
- MAIL：接收通知的邮箱。示例：`mail@mail.com`






### 测试运行

- 在GitHub仓库的“Actions”选项卡中，手动触发运行一次工作流程。
- “Actions”页面>"Run SSH Login">"Run workflow">"Run workflow"
- 检查运行结果，没有报错说明就是运行成功了，可以点击运行记录的列表进去查看运行的详细情况



### 定时自动运行

- 此工作流默认每月的 5号 北京时间 19 点运行

- 可以根据自己的需求调整运行时间

  ```yaml
  - cron: '0 11 5 * *'  # 每月的 5号 北京时间 19 点运行
  ```

