# 花店 AI Skills

为 Codex 收纳和分发花店运营相关技能。每个技能放在 `skills/<skill-name>/` 下，后续可继续添加新技能。

## 当前技能

- `skills/flower-shop-daily-chat-review`：通过 Codex Computer Use 读取已登录的 macOS 微信界面，按日期整理客户对话并复盘花店运营。只在用户发起时运行；默认跳过未读会话，避免误清未读状态。
- `skills/flower-shop-multiplatform-ops`：分析美团、抖音与麦芽田提供的店铺、订单、配送和评价数据，生成商品/活动建议、短视频内容和多平台运营日报；用户明确要求时，可通过 Computer Use 操作已登录后台中的可见功能。

## 安装

在 Codex 中让 AI 安装这个仓库里的技能：

> 请从 GitHub 仓库 `feyakit/flower-shop-ai-skills` 安装 `skills/flower-shop-daily-chat-review`。

安装多平台运营助手：

> 请从 GitHub 仓库 `feyakit/flower-shop-ai-skills` 安装 `skills/flower-shop-multiplatform-ops`。

也可以把对应技能文件夹复制到个人技能目录：

```text
~/.codex/skills/flower-shop-daily-chat-review/SKILL.md
```

## 上游技能库备份

以下两个仓库已在 `feyakit` 账号下建立 GitHub fork，保留各自的完整仓库与上游来源；它们是独立仓库，不是本仓库的子目录：

- [codex-skills-collection（我的备份）](https://github.com/feyakit/codex-skills-collection) ← 上游：[2669095290-prog/codex-skills-collection](https://github.com/2669095290-prog/codex-skills-collection)
- [xiaohongshu-skills（我的备份）](https://github.com/feyakit/xiaohongshu-skills) ← 上游：[autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills)

换电脑安装时，可从自己的 fork 安装相应技能。例如：

> 请从 `feyakit/codex-skills-collection` 安装 `skills/flower-shop-management`。

> 请从 `feyakit/xiaohongshu-skills` 安装 `skills/xhs-publish`。

更新备份时，在相应 fork 中从 GitHub 的 **Sync fork** 同步上游更新；更新后还需在本机重新安装技能副本。

`codex-skills-collection` 上游没有附带许可证文件，因此保留为独立 fork 并注明来源；未经作者许可，不把其文件复制到本仓库再分发。

## 使用要求

- 需要 Codex Computer Use。
- 微信聊天复盘技能当前面向 macOS 微信桌面端，使用者需要在自己的电脑上登录微信。
- 技能读取使用者自己界面中可见的聊天内容，不会包含仓库作者的聊天记录或账号凭证。
- 这是按需前台流程，不是后台常驻同步。
