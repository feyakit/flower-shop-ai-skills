# 花店 AI Skills

为 Codex 收纳和分发花店运营相关技能。每个技能放在 `skills/<skill-name>/` 下，后续可继续添加新技能。

## 当前技能

- `skills/flower-shop-daily-chat-review`：通过 Codex Computer Use 读取已登录的 macOS 微信界面，按日期整理客户对话并复盘花店运营。只在用户发起时运行；默认跳过未读会话，避免误清未读状态。

## 安装

在 Codex 中让 AI 安装这个仓库里的技能：

> 请从 GitHub 仓库 `feyakit/flower-shop-ai-skills` 安装 `skills/flower-shop-daily-chat-review`。

也可以把对应技能文件夹复制到个人技能目录：

```text
~/.codex/skills/flower-shop-daily-chat-review/SKILL.md
```

## 使用要求

- 需要 Codex Computer Use。
- 微信聊天复盘技能当前面向 macOS 微信桌面端，使用者需要在自己的电脑上登录微信。
- 技能读取使用者自己界面中可见的聊天内容，不会包含仓库作者的聊天记录或账号凭证。
- 这是按需前台流程，不是后台常驻同步。
