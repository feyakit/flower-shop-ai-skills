# 花店 AI Skills

花店运营的全套 AI 技能，**13 个技能全部在这一个仓库里**。每个技能是 `skills/<skill-name>/` 下的独立目录：`SKILL.md`（带 YAML frontmatter）+ 可选的 `references/`（规则、playbook）、`templates/`（交付模板）、`scripts/`（Python / Shell / PowerShell）、`assets/`（示例配置），可直接给 Codex 或 Hermes 当技能用。

## 技能清单

| # | 技能 | 分类 | 干什么 | 什么时候用 |
|---|---|---|---|---|
| 1 | `flower-shop-copywriting` | 内容 | 小红书文案包：标题公式、正文、话题标签、封面字、本地搜索词、买方场景角度 | 只要文案（标题/正文/标签），不管发不发 |
| 2 | `xhs-flower-shop-growth` | 内容 | 获客型内容：标题正文话题标签、爆款标题公式、城市定制（成都/南通/上海/北京） | 做拉客内容、要爆款标题思路 |
| 3 | `xhs-flower-draft-workflow` | 内容 | 端到端成品流程：图优化 → 本地获客标题正文 → 按「城市优先 + 购买意图」选话题 → 存草稿箱；cookie 运行时传入、不写死 | 要一条龙做到草稿箱 |
| 4 | `chengdu-flower-xhs-draft` | 内容 | 成都花店一条龙：花束照片轻修图 → 20 字左右带 emoji 标题（以「成都花店」结尾）→ 正文+可见话题 → 存草稿箱并验稿 | 给成都花店发小红书、要存草稿箱 |
| 5 | `flower-shop-image-optimization` | 图片 | 批量修花图：自然校色、花束提亮、轻锐化、EXIF 方向、3:4 / 4:5 裁切、1080×1440 或 1080×1350 导出、小体积上传版 | 图暗/乱，要出可发布的成品图 |
| 6 | `flower-arrangement-learning` | 花艺 | 花艺诊断与改法：用商业花艺师框架点评花束（包装/配色/层次/焦点），给修改方向和改进参考图 | 问“这束花哪里不对 / 花艺师会怎么改” |
| 7 | `flower-shop-chat-replies` | 客服 | 客服话术：询价、嫌贵、配送时间、定制、确认订单、投诉售后的高转化回复 | 客户发消息/聊天截图，问怎么回 |
| 8 | `flower-shop-daily-chat-review` | 客服 | 微信聊天复盘：用 Computer Use 读已登录的微信桌面版，按天整理客户对话：问了什么、哪些单没成、售后情况 | 说“看今天的聊天/整理客户对话” |
| 9 | `flower-shop-management` | 经营 | 花店经营/订单：录单、聊天转订单、排单配送、多地区筛选、配送单打印、客户跟进、售后复盘、日报 | 要排单/打配送单/理订单 |
| 10 | `flower-shop-multiplatform-ops` | 经营 | 多平台经营：美团、抖音、麦芽田的店铺诊断、商品与活动、后台操作（Computer Use）、评价回复、订单配送分析、跨平台报表 | 管美团/抖音/麦芽田店铺 |
| 11 | `flower-shop-juguang` | 投放 | 聚光投放：单/多账号花费分析、token 刷新、开口成本与线索成本诊断、创意评分、预算出价建议、飞书销售反馈解读、执行前预览 | 看聚光数据、调预算出价、筛创意 |
| 12 | `flower-shop-account-optimization` | 账号 | 账号诊断报告：小红书账号定位、内容矩阵、置顶笔记、转化路径、哪些笔记适合投聚光，输出 HTML/Word/Obsidian 报告 | 要看花店账号/做账号优化方案 |
| 13 | `xhs-flower-workbench-deploy` | 交付 | 工作台交付部署：小红书 AI 花店工作台的客户侧部署流程，含报价单、交付方案、客户手册、三色清单模板 | 给客户装/部署工作台 |

## 四个内容技能怎么挑

- 只写内容、不要动手发 → `flower-shop-copywriting`
- 要一条龙做到草稿箱、含话题排序规则 → `xhs-flower-draft-workflow`
- 客户在成都、标题要按成都规则（结尾「成都花店」+ emoji） → `chengdu-flower-xhs-draft`
- 重点是拉本地客、要爆款标题公式与城市定制 → `xhs-flower-shop-growth`

## 安装

### Codex

整目录拷到个人技能目录：

```bash
git clone https://github.com/feyakit/flower-shop-ai-skills.git
cp -r flower-shop-ai-skills/skills/<skill-name> ~/.codex/skills/
```

也可以直接让 Codex 装：

> 请从 GitHub 仓库 `feyakit/flower-shop-ai-skills` 安装 `skills/flower-shop-copywriting`。

### Hermes

放到 Hermes 的技能目录，例如 `~/.hermes/skills/<skill-name>/`、profile 的 `skills/`（如 `/opt/data/profiles/default/skills/`），或本机的 `/opt/data/skills/<skill-name>/`：

```bash
cp -r flower-shop-ai-skills/skills/<skill-name> ~/.hermes/skills/
```

带 `references/`、`templates/`、`scripts/`、`assets/` 的技能要整目录一起拷，别只拿 `SKILL.md`；`agents/openai.yaml` 是给 Codex 的元数据。

## 校验

`MANIFEST.sha256` 是仓库内全部文件的 SHA-256，解压/克隆后在仓库根目录自检：

```bash
shasum -a 256 -c MANIFEST.sha256     # macOS
sha256sum -c MANIFEST.sha256         # Linux
```

## 使用要求

- 需要 Codex Computer Use：`flower-shop-daily-chat-review`、`flower-shop-multiplatform-ops`、`xhs-flower-draft-workflow` 等要操作可见界面的技能。
- 微信聊天复盘面向 macOS 微信桌面端，使用者要在自己电脑上登录微信；技能只读你自己界面里可见的聊天内容，不含作者的聊天记录或账号凭证。
- `flower-shop-juguang` 需要聚光 API token（带刷新流程）；`references/xiaohongshu_config.example.json` 只是示例，真实配置别提交进仓库。
- 任何需要小红书 cookie / 微信登录的技能，凭据都在运行时提供，仓库里不写死、不硬编码。
- 这些都是按需前台流程，不是后台常驻同步。

## 凭据不入库

仓库只放 `*.example.*`；以下文件已在 `.gitignore` 中挡住：

- `xiaohongshu_config.json`、`xiaohongshu_token*.json`、`*token*.json`
- `.env`（`*.env.example` 除外）
- `*.cookies`、`cookies*.json`

## 目录明细

<details>
<summary>逐个技能的文件构成</summary>

**`flower-shop-copywriting`**（4 个文件）
```
SKILL.md
agents/openai.yaml
references/content-and-topics.md
references/title-formulas.md
```

**`xhs-flower-shop-growth`**（4 个文件）
```
SKILL.md
agents/openai.yaml
references/content-and-topics.md
references/title-formulas.md
```

**`xhs-flower-draft-workflow`**（7 个文件）
```
.gitignore
SKILL.md
agents/openai.yaml
references/account-cookies.md
references/draft-save.md
references/image-copy-workflow.md
references/topic-selection.md
```

**`chengdu-flower-xhs-draft`**（7 个文件）
```
SKILL.md
agents/openai.yaml
references/body-template.md
references/draft-verification.md
references/title-rules.md
scripts/optimize_xhs_image.ps1
scripts/optimize_xhs_image.sh
```

**`flower-shop-image-optimization`**（5 个文件）
```
SKILL.md
agents/openai.yaml
references/photo-optimization-playbook.md
scripts/optimize_flower_images.py
scripts/requirements.txt
```

**`flower-arrangement-learning`**（3 个文件）
```
SKILL.md
agents/openai.yaml
references/evaluation-framework.md
```

**`flower-shop-chat-replies`**（3 个文件）
```
SKILL.md
agents/openai.yaml
references/scene-playbook.md
```

**`flower-shop-daily-chat-review`**（1 个文件）
```
SKILL.md
```

**`flower-shop-management`**（6 个文件）
```
SKILL.md
agents/openai.yaml
assets/flower_order_hub.env.example
references/order-management-playbook.md
scripts/flower_order_hub/flower_order_hub.py
scripts/flower_order_hub/index.html
```

**`flower-shop-multiplatform-ops`**（2 个文件）
```
SKILL.md
agents/openai.yaml
```

**`flower-shop-juguang`**（23 个文件）
```
SKILL.md
agents/openai.yaml
references/best_practices.json
references/optimization_rules.md
references/xiaohongshu_config.example.json
scripts/__init__.py
scripts/xhs_multi_account.py
scripts/xiaohongshu_advanced_analytics.py
scripts/xiaohongshu_ai_assistant.py
scripts/xiaohongshu_ai_brain.py
scripts/xiaohongshu_attribution_ai.py
scripts/xiaohongshu_auto_executor.py
scripts/xiaohongshu_automation_rules.py
scripts/xiaohongshu_creative_ai.py
scripts/xiaohongshu_creative_analyzer.py
scripts/xiaohongshu_expert_knowledge.py
scripts/xiaohongshu_juguang_sdk.py
scripts/xiaohongshu_keyword_manager.py
scripts/xiaohongshu_real_ai.py
scripts/xiaohongshu_reports.py
scripts/xiaohongshu_sdk_enhancer.py
scripts/xiaohongshu_self_learning.py
scripts/xiaohongshu_smart_optimizer.py
```

**`xhs-flower-workbench-deploy`**（10 个文件）
```
SKILL.md
references/client-app-install.md
templates/三色清单.html
templates/三色清单示例.pdf
templates/交付文档.md
templates/交付方案.html
templates/客户使用手册.html
templates/报价单-交付清单.html
templates/报价单-交付清单示例.pdf
templates/需求沟通提纲.html
```

</details>

## 来源

本仓库集中存放花店技能，取代之前分散的副本与 fork。部分技能内容源自公开的技能合集仓库（上游未附 LICENSE 文件），此处保留原样并注明来源，供自用与客户交付；如需对外再分发，请自行确认原作者的授权。
