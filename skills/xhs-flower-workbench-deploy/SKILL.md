---
name: xhs-flower-workbench-deploy
description: "Use when deploying the 小红书 AI 花店工作台 for a client."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [xiaohongshu, codex, deployment, client-delivery, flower-shop]
---

# 小红书 AI 花店工作台：客户交付

客户眼里的“AI 运营工作台”，实际是 Codex 桌面版 + 两个 skill 仓库 + 一个 Chrome 扩展 + Obsidian。
**90% 是提示词，真技术只有桥接那一段。** 手册会把它写得很玄，别跟着玄。

仓库：
- `autoclaw-cc/xiaohongshu-skills`（MIT，桥接引擎 + 扩展）
- `2669095290-prog/codex-skills-collection`（11 个花店提示词，含聚光、草稿工作流、客服话术）

## When to Use

- 客户（花店/单店）拿一份「AI 运营工作台」手册来，问能不能实现、多少钱、怎么落地
- 要把小红书内容生产 + 填表后台这条线部署到客户的 Windows/Mac 上
- 要给客户报价、划清做什么不做什么、写交付文档与客户使用手册
- 客户顺带提周边需求（美团、小程序、聚光、NAS、手机端、竞品分析），要判断接不接、怎么单独算

## 链路与唯一的验收闸门

```
CLI(scripts/cli.py) → ws://localhost:9333(bridge_server.py) → Chrome 扩展 XHS Bridge → 页面 DOM
```

- CLI 会**自己拉起** bridge_server，不用单独启动；有单实例锁。
- 唯一的验收闸门：`uv run python scripts/cli.py check-login` 返回客户昵称。**它不过就停下修桥接，别往下做。**
- `fill-publish` 填表 / `click-publish` 才点发布 —— 用这个分步设计把“发布”这一步留给客户本人。

## 必踩的六个坑

**1. 海外或机房 IP 会被小红书屏蔽（最隐蔽）**
`www.xiaohongshu.com` 返回 404、浏览器被跳到 `www.rednote.com`、`creator.xiaohongshu.com` 返回 200 但 `<div id="app">` 是空的、截图纯白，于是 `fill-publish` 报 `Bridge 错误: 页面加载超时`。
→ **发布链路只能在客户国内网络下验证**；扩展和桥接在海外照样能通，别据此下“装坏了”的结论。
→ 客户梯子必须让小红书**直连**，不能全局代理。预检第一项就是“她能用手动打开小红书后台并看见内容吗”。

**2. 扩展到 rednote.com 就失能**
manifest 只授权 `xiaohongshu.com`，跳国际站后报
`Cannot access contents of url "https://www.rednote.com/". Extension manifest must request permission to access this host.`
→ 把 `https://*.rednote.com/*` 加进 `host_permissions`，并加进 `content_scripts.matches`。

**3. 扩展加载没法脚本化**
`chrome://extensions` 是浏览器内部页面，脚本点不了。两条路：`--load-extension` 启动参数（**用独立 `--user-data-dir`，别动客户日常 profile**；Chrome 已在跑会忽略该参数，先退出），或打包 crx + 企业策略强制安装（重，只有做产品才值得）。

**4. 9333 端口单实例**
重复开任务会 `OSError: [Errno 98] address already in use`。清理时 `pkill -f "bridge_serve[r].py"` 这种带字符类的写法——普通 `pkill -f bridge_server.py` 会匹配到你自己那条 shell 命令行并把它杀掉（表现为命令 exit -15）。

**5. 老 Mac（如 2015 Intel，macOS 12 Monterey）装不了原版 App**
ChatGPT/Codex 桌面版强制 **macOS 14+**，且 **Chrome 151+ 已于 2026 年中放弃 macOS 12**（最后一版为 Chrome 150）。强拖或改 plist 会因缺系统库直接闪退。
→ 路线 ①（客户坚持用原 App，且硬件 ≥ 16G + 纯集显）：用 OCLP 升 **macOS 14 Sonoma**（别追 15），**必须另建独立 APFS 宗卷保留原 12.7.6**（需 ≥ 40GB），升完用 iPhone USB 共享网络跑 Post-Install Root Patch 恢复 Wi-Fi，再彻底关闭自动更新。
→ 路线 ②（不动原系统零风险）：留在 12.7.6 用 Chrome 150 + Codex CLI（支持 macOS 12+Intel）+ 本地 Web UI 壳，桌面放两个图标。

**6. Codex 首次启用必过海外手机号验证（`auth.openai.com/add-phone`）**
普通 ChatGPT 聊天可用干净 IP + Apple/Google 登录免手机，但**桌面版进 Codex 必须验海外手机号**——买了 Plus 也跳不过，+86 报 `invalid_phone_number`，Google Voice 等 VoIP 被拦截；部分东南亚号段默认发到 WhatsApp 导致接码失败，优先用美/英/日实体卡或只走 SMS 的号段。首次通过后日常靠邮箱登录，**务必在交付前先帮客户过掉这关**，别带到现场卡死。

## 报错对照（给客户的一页纸，打印出来）

| 屏幕上的话 | 真实原因 | 客户自己能做的 |
|---|---|---|
| `Extension 未连接，请确认浏览器已安装并启用 XHS Bridge 扩展` | 扩展被禁用、没加载、Chrome 没开 | `chrome://extensions` 看 XHS Bridge 是否开启 → 重启 Chrome |
| `Cannot access contents of url … must request permission` | 被跳到未授权域名（rednote.com） | 关掉梯子全局模式 |
| `页面加载超时` | 页面本身没加载出内容 | 先手动打开同一地址，能看见内容再重试 |
| 端口 9333 被占用 / 两个窗口互相干扰 | 开了两个任务 | 只留一个对话窗口 |
| 文案没写进后台 | 小红书改版，选择器失效 | 找交付方修（客户修不了） |

## 内容层的高频失败

- 图片用**绝对路径**、目录纯英文无空格（中文名、iCloud 未下载的文件都会失败）；3:4 竖图、3–9 张。
- 小红书标题按 UTF-16 计 20 字，emoji 占两位，超了直接截。
- 网页版 `xiaohongshu.com` 与 `creator.xiaohongshu.com` 必须同一账号；客户 Chrome 常登两三个号，选错就把内容填进别人的后台。
- 一天一条、人点发布。项目自带 `human.py` 只是节奏模拟，不是风控盾。

## 交付形态：脚本，不是让 AI 装

装环境是“下载+解压+写文件”，脚本 30 秒；让 AI 做会边读日志边试错，六分钟起步还可能改坏 PATH。
分三层：`install.ps1`/`install.sh`（90%）→ `verify.sh`（自检 uv/repo/端口/网络）→ `diagnose.md`（客户把报错粘进 AI 让它定位，AI 擅长诊断不擅长装）。

- 国内杀软（360/火绒）会拦 PowerShell 脚本，用 `.bat` 包一层或给 exe。
- 脚本首行查管理员权限，否则 UAC 不弹会静默失败。
- 客户电脑上必须**主动告知一件事**：以后从哪个快捷方式开 Chrome（带 `--load-extension` 的那个），否则他从老图标开就没扩展，会当成“你装的东西坏了”。

## 远程方式怎么选

- 首次交付首选 **UU 远程**（网易）：基础远控免费、不限时长、被协助方**不用注册账号**，画质能看清后台和二维码；向日葵免费版压到 720P 以下，二维码常扫不出。ToDesk 免费版 80 小时/月够用但没优势。
- 引导客户：「设置 → 安全 → 允许他人远程协助 → 远程协助 → 开始协助」，把本设备 ID + 临时验证码发你；协助端（你）登录，被协助端不用注册。
- **UAC 弹窗会让远程画面黑屏**：装 ChatGPT 桌面版、装 uv 都要管理员权限，一旦弹 UAC，Windows 切到安全桌面，你就看不见也点不了。让客户**右键图标「以管理员身份运行」再开客户端**，它才带管理员令牌接管弹窗。这条不做，装到一半必卡。
- 开工前让客户把电源计划改成「永不睡眠」，收工改回；用完让他刷新临时验证码。
- **不要把客户电脑拿回家**——里面有微信、相册、聊天记录，出事说不清。
- 维护期：装完顺手留 SSH。
- Tailscale **只是网络层**，装完 5 分钟但要再叠一层才能用：跑命令要 sshd（Windows 默认没有），看屏幕要 RDP（**Win 专业版才有，家庭版没有**，家庭版还得装 VNC 又被杀软拦）。
- 别让客户登你的 Tailscale 账号（他能看到你所有设备）；发邀请让他用自己的 Google/微软账号接受。

## 能力边界（对客户必须当面划清）

- 能做：文案/标题/话题、配图、填进后台、客服话术分析、复盘进 Obsidian、手工填表后的数据分析。
- 不做：自动发布、自动回私信/微信、无人值守、承诺涨粉或成交、代持账号密码。
- 小程序先问清是三选一：SaaS（有赞/微盟/小商店 → 只做内容）、有源码（= 开发项目，另立项报价）、无后台（做不了）。
- 聚光开放 API 要品牌/服务商资质，个人花店拿不到 → 数据永远靠人填或截图。
- 报价：部署一条线一个价；美团/聚光/小程序**单独算不打包**，多一条线多一个失败点而售后还是 7 天。
- **美团**：只做评价回复、商品/团购文案、后台导出 CSV 后的分析；改价、上下架、核销、退款一律不接——小红书发错删掉即可，美团改错价格是按单赔钱。美团开放平台要服务商资质，个人拿不到。
- **麦芽田**（maiyatian.com，北京麦芽田）：第三方订单/自配送 SaaS，鲜花是其主力类目。商家后台是网页 `saas.maiyatian.com`（账号密码 / 手机验证登录），另有 PC 客户端、Android/iOS（uni-app 打包）、手机触屏版；内有**报表中心、数据魔方、商品助手、库存、成本核算**。开放平台（`open-api.maiyatian.com`）**只对渠道方与配送服务商**，接口只有「推单进麦芽田 / 回传配送轨迹 / 聚合配送」——**没有商家侧经营数据接口，也没有商品编辑接口**。所以「自动看数据 + 自动改商品」只能界面自动化，且它里面装着客户全部渠道订单，被限制比小红书封号严重 → 优先客户自己电脑/家庭网络跑，用子账号。
- **NAS 需求先翻译**：客户说「要一台 NAS」，实际要的常是「手机/平板/电脑都能看照片」。真需求是三选一：只想随时看 → 云盘（几百/年）；要手机相册自动备份、数据自己持有 → 成品双盘 NAS（极空间/绿联自带内网穿透，无公网 IP 也能外网访问；群晖 QuickConnect 免费但慢）；自建 TrueNAS/OMV 只适合你亲自维护。报价 800–1200 装机调试，**硬件让客户自购，别代购**（价格波动、售后、发票都是雷）。
- NAS 与工作台的真正协同点：手机拍完自动进 `/素材/日期/` → 电脑挂载网络盘 → AI 直接读。**“素材断供”是这类项目最高频的死法**，讲这一条比讲 RAID 有用。
- **竞品分析/视频生产不是现成一条龙**：取数用 MCP（小红书 `xpzouying/xiaohongshu-mcp`、抖音托管只读的 `zen-studio-labs/douyin-mcp`），出片用 `jnMetaCode/openshorts` 或 ffmpeg 模板，中间要自己串。**`xiaohongshu-mcp` 与 `xhs-bridge` 抢登录态**（同账号不能多端网页同时登录），二选一。
- 花店视频别用 AI 文生视频：卖真花，生成假花客户到店就穿帮。走「3–6 张实拍 + TTS 配音 + 字幕模板 → mp4」，可控、零成本、5 秒出片。

## 本机生成交付文档（PDF）

`chrome --print-to-pdf` 在这台机器上会挂死（`CompositePages: Cannot create new shared memory region`），别再试。改用 `browser_exec`：

```python
new_tab("file:///<绝对路径>.html"); wait_for_load()
res = cdp("Page.printToPDF", printBackground=True, paperWidth=8.27, paperHeight=11.69,
          marginTop=0, marginBottom=0, marginLeft=0, marginRight=0, preferCSSPageSize=True,
          displayHeaderFooter=True, headerTemplate="<div></div>",
          footerTemplate="<div style='font-size:7.5pt;color:#8a8f98;width:100%;text-align:center'>标题　<span class='pageNumber'></span>/<span class='totalPages'></span></div>")
open(out, "wb").write(base64.b64decode(res["data"]))
```

中文字体在 `/opt/data/home/.fonts`（Source Han Sans SC + 文泉驿），`@page { size: A4 }` 直接生效。

**分页**：不要用 `<div class="pb" style="break-before:page">` 强制分页——它会把正文切成只剩一行的残页。改用自然流 + `h2{break-after:avoid}`、`table,pre,.callout{break-inside:avoid}`、`tr,li{break-inside:avoid}`，再用 `pypdf` 逐页 `extract_text()` 数字符数，某页只有几十字就是分页事故，回去收紧行高/边距。

**避头尾自检（必做）**：中文标点落在行首（`,` `。` `——`）肉眼很难发现，用 DOM 逐字符量矩形，跑完要求 0 处：

```javascript
(() => { const bad="，。、；：？！）」』】》,.;:?!)]}";
  const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT); let n,h=[];
  while(n=w.nextNode()){ const t=n.nodeValue; if(!t||!t.trim())continue;
    for(let i=1;i<t.length;i++){ if(!bad.includes(t[i]))continue;
      const a=document.createRange();a.setStart(n,i-1);a.setEnd(n,i);
      const b=document.createRange();b.setStart(n,i);b.setEnd(n,i+1);
      if(b.getBoundingClientRect().top-a.getBoundingClientRect().top>6)h.push(t.slice(Math.max(0,i-10),i+6)); }}
  return JSON.stringify({violations:h.length,sample:h.slice(0,5)}); })()
```

写 HTML 时还会踩两个坑：CSS 里加 `line-break: strict` 能挡掉大部分；**正文里误留 markdown 的 `**加粗**` 会原样显示成星号**，写完 grep 一遍 `**` 替换成 `<b>`；`<b>…</b>` 后面紧跟句号容易挤到下一行，把句号写进 `<b>` 里面。

## 交付物三件套（分开给，别混）

| 文件 | 给谁 | 写什么 |
|---|---|---|
| 需求沟通提纲 | 你自己 | 开场话术、能做/不做两栏、8 个必问问题、报价与加价项 |
| 交付方案 | 你自己 | 架构链路、实测结论、九步流程、报错表、能力边界、风险与未验证项 |
| 客户使用手册 | 客户（贴桌上） | 每天四件事、三句话术、改稿说法、六行排错表、三件红线、打勾清单 |

**客户版全文不出现任何技术词**（uv、端口、扩展、选择器、manifest 一律不写）。她的世界里只有三个入口：聊天框、素材文件夹、经验库。出现技术词她就怕，怕了就不用了。文档里标「未验证」的项（发布选择器、国内渲染、macOS 扩展加载）不得对客户说成已经可用。

## 客户「什么都想要、以为 AI 万能」怎么处理

低文化水平的客户不是靠讲道理说服的，靠**一张纸 + 一次演示**。

1. **再不用「不能」这个词。** 她听见「不能」= 你不愿意 / 你水平不够。一律翻译成「这个要另外做，另算钱、另排期」。需求不会消失，只会变成有价钱的需求。
2. **三色清单是主道具。** 把她的所有要求写进绿/黄/红三栏（模板 `templates/三色清单.html`），打印贴墙上。她再提新想法时，让她「指一个颜色」，而不是听你解释。物理道具比口头解释有效，因为她记不住话但记得住颜色。红栏每条前面加 `✕`，否则她会把「不替她发笔记」读成一项可购买的服务。
3. **打卡「接口」这个词。** 她以为 AI 能接任何系统，是因为她把 AI 当人。换成：**「每个平台都有一道门，只有店主本人有钥匙，我只能在门口递东西。」** 顺带把 AI 的定位钉死：**「记性特别好的学徒，教过的做得又快又好，没教过的不会自己琢磨，还会一本正经胡说」** —— 这一句同时治「万能期待」和「AI 幻觉」。
4. **让她自己说出「不能」。** 比你说十遍管用：她要自动回私信，你问「客户问 199 的花，它答 299，你赔不赔？」她要自动发笔记，你问「发错一条，你自己删用几秒？我发错你找谁？」结论由她下，责任就不在你。
5. **一次只给一个甜头。** 她要十个功能，你只做第一个并做到她惊讶，其余的说「先把这个用熟」。她的工作记忆只装得下三步。
6. **语音 > 文字。** 看字费劲的人，60 秒语音胜过三页文档；说完让她复述一遍（「咱今天做几件事？」），点头不等于听懂。
7. **把加需求变成动作。** 清单底部留「想加的写在这」横线 + 一句「我按顺序排，不插队、不白干」。要付钱、要写字的时候，欲望自己会收。
8. **报价不打包。** 多一条线多一个价，说成「多开一个窗口多一份工钱」。

## 客户要自己用 Codex：卖环境，不卖聊天框

客户说「我想自己用 Codex 干这些」时，你交付的是**隔离的环境 + 技能包 + 一张触发卡**，不是教他天天跟 AI 聊天。

- 交付形态错了就变苦力：让他自己开对话框说「去帮我导报表」，他要会开、会说、会等、卡住了要找你 → 用三次就废。正确形态是一次性配好技能 + 快捷方式，他看到的是「双击 → 早上多一份日报」。
- **三条硬规矩**：① 只给三个固定文件夹的权限（素材/报表/输出），他电脑里有微信和客户资料；② 开审批模式，不开全自动（他不会看日志）；③ 不代持账号——用他自己的 ChatGPT/API key，别让他登你的号。
- **技能是模型读的说明书，不是菜单**。装上不等于能用，还差三样：工具能力、登录态、**触发词**。交付必须附「三张卡」，每张一句客户照读的原话，卡底写「如果它说没听懂，就把这句话原样再发一遍」。
- 技能 description 常是英文，而客户只会说中文：把客户原话写进 description，否则弱模型下触发会漏。
- Codex 技能里的 `cua.getApp("com.tencent.xinWeChat")` / `getAXState()` 是 **cua-driver 的 JS 词汇**；搬到 Hermes 要改写成 `computer_use(action="capture"/"click", element=N)` 那套，直接抄会跑不通。
- 本机（Hermes 容器）没有桌面：`DISPLAY` 为空、无 Xvfb/xdotool/x11vnc → `computer_use` 在这里跑不了；能用的只有 `browser_exec` 和 adb 盒子（`localhost:5555`）。要在这边演示就得走这两条。
- 技能**不随任何账号同步**（Codex `~/.codex/skills`、Claude `~/.claude/skills`、Hermes `$HERMES_HOME/skills` 都是本地文件），客户换电脑必须重装 → 用私有仓库 + `git pull` 当「云同步」，只放技能，不放客户数据。
- **在 Codex 里调教新技能的正确闭环**：先在普通对话里用真实素材磨 2–3 轮到完全满意 → 在同一轮让 Codex 调 `$skill-creator` 写入 `~/.codex/skills/<name>/SKILL.md`（触发/不触发边界写进简洁 `description`，店名/地址/价目/爆款样稿拆进 `references/` 方便跨客户替换）→ **必须新开一轮对话冷启动验收**（当轮写完不自动重载）。
- 报价：一次性环境搭建 + **年度维护**（Codex 会升级、界面会变、他会换电脑，这些都会回来找你）。合同写明「不承担数据与经营损失」「界面改版失效另议」。

## templates/ 与 references/

- `templates/三色清单.html` + `三色清单示例.pdf` —— 给「文化水平低、什么都想要」的客户看的 A4 单页：绿（今天就能做）/ 黄（另排期另算钱）/ 红（不接，给替代）。**这是这类客户的核心道具，见下一节。**
- `templates/交付文档.md` —— 施工单（预检、九步、报错表、验收、后续收费项）
- `templates/需求沟通提纲.html` —— 客户沟通一页纸（开场话术、能做/不做、8 个问题、报价）
- `templates/交付方案.html` —— 完整方案（架构图、实测结论、流程、风险），6 页
- `templates/客户使用手册.html` —— 客户版（无技术词、可打印上桌），3 页
- 以上 HTML 都用「本机生成交付文档」那套 CDP 方式转 PDF，交付前跑一遍避头尾自检。
- `references/client-app-install.md` —— 客户怎么在 iPhone 上装 ChatGPT（PWA 优先、美区 ID、代注册、绑卡为什么失败、礼品卡付费）
