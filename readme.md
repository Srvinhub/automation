# SSH Login Workflow

管理和自动化多个服务器的登录信息及推送通知。

---

## 🌟 配置 Secrets

在 GitHub 仓库中完成以下步骤：

1. **导航到 `Settings > Secrets and variables > Actions`**。
2. 点击 **“New repository secret”**，添加以下内容：

### 必需 Secrets

| Secret 名称            | 描述                                    | 示例                                   |
|-------------------------|-----------------------------------------|----------------------------------------|
| `SSH_INFO`             | 包含 SSH 连接信息的 JSON 字符串        | `[ {"hostname": "s5.serv00.com", "username": "user", "password": "password"} ]` |
| `TELEGRAM_BOT_TOKEN`   | 您的 Telegram Bot API Token            | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `TELEGRAM_CHAT_ID`     | 您的 Telegram Chat ID                  | `123456789`                            |
| `PUSH`                 | 推送渠道，支持 `mail` 或 `telegram`    | `mail`                                 |
| `MAIL`                 | 接收通知的邮箱地址（仅适用于 `mail`） | `example@mail.com`                     |

---

## 🚀 测试工作流

1. **手动运行工作流**：
   - 进入 GitHub 仓库的 **Actions** 页面。
   - 点击 **“Run SSH Login”**。
   - 在右侧选择 **“Run workflow”** 按钮。

2. **查看运行结果**：
   - 运行完成后，检查是否有报错。
   - 点击运行记录查看详细日志。

---

## ⏰ 定时运行

默认配置为每周一 **北京时间 0 点** 自动运行。

### 修改运行时间

您可以根据需求调整运行时间，修改工作流文件中的 `cron` 表达式。例如：
```yaml
schedule:
  - cron: '0 16 * * 0'  # 每周一 北京时间 0 点运行
```

更多 `cron` 表达式配置指南，请参考 [GitHub Actions 官方文档](https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#schedule)。

---

## 📚 参考

- [GitHub Actions 入门指南](https://docs.github.com/en/actions)
- [Paramiko 官方文档](https://docs.paramiko.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

使用此工作流，轻松管理您的服务器登录信息和通知推送！

