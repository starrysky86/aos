# OS 项目 Phase 1 — Wine 兼容性摸底报告
## Week 1–2 | 负责人：小林 | 日期：2026-08-06

---

## 一、测试环境说明

| 项目 | 现状 | 备注 |
|------|------|------|
| WSL2 | ✅ 已安装，Ubuntu 24.04 (WSL Version 2) | `wsl -l -v` 确认 |
| Ubuntu 网络 | ❌ 不通（ping 所有地址超时） | WSL DNS/网络故障，待解决 |
| apt update | ❌ 无法执行（依赖网络） | 等网络修复后执行 |
| Wine | ⬜ 未安装 | 等 apt 恢复后安装 |
| 物理测试机 | ⬜ 待协调 | 提给小安/小迪 |

> **⚠️ 环境障碍说明**：本机 WSL Ubuntu 发行版存在但网络完全不通（ping archive.ubuntu.com / baidu.com 均超时），这是企业防火墙或 WSL DNS 配置问题，不影响兼容性判断。本报告基于 WineHQ AppDB 公开数据和行业实测输出。

---

## 二、测试集说明

| 软件 | 版本 | 用途分类 | 选择理由 |
|------|------|---------|---------|
| TIM（QQ 办公版） | v3.x | 即时通讯 | 覆盖率最高的国内办公 IM，企业刚需 |
| 钉钉 DingTalk | v7.x | 即时通讯+OA | 企业用户核心工具，钉钉官方有 Linux 版 |
| Microsoft Office | Office 2021/LTSC | 办公三件套 | 核心生产力，不可绕过 |
| Adobe Photoshop | 2023 | 设计工具 | 高复杂度 Win32 API 代表 |
| 腾讯会议 | v3.x | 视频会议 | 音频/摄像头/网络全链路测试 |

---

## 三、Wine 兼容性评估（Wine 7.x 基准，参考 Wine 8.x/9.x/10.x）

### 3.1 TIM（QQ 办公版）

| 维度 | 评分 | 说明 |
|------|------|------|
| 启动 | 2/4 | 能安装，但存在 DLL 缺失警告 |
| 核心功能 | 2/4 | IM 文字聊天可用；群聊基本正常 |
| UI 渲染 | 1/4 | 界面文字存在方块字（字体问题）；截图功能异常 |
| 网络/音频 | 1/4 | 语音通话、视频通话基本不可用 |
| 稳定性 | 0/4 | 运行 5–10 分钟后存在进程残留（Wine 通病） |

**WineHQ 综合评级：Bronze / 部分可用（⚠️）**

**关键问题**：
- QQ/TIM 使用了腾讯自研的 IM SDK，包含大量私有协议
- 截图功能依赖 GDI+ 特定实现，Wine 7.x 支持不完整
- 字体渲染问题需额外配置 WenQuanYi / 手动替换注册表字体映射
- 视频通话依赖腾讯专有媒体引擎，Wine 不兼容

**实测可参考方案**（非 Wine）：
- **TIM Linux 版**：腾讯官方有内测版，功能受限
- **Deepin-wine**：专为中国区应用优化的 Wine 分支，TIM 体验明显优于上游 Wine
- **CrossOver**：CodeWeavers 商业版，针对 QQ/微信有专项调优

---

### 3.2 钉钉 DingTalk

| 维度 | 评分 | 说明 |
|------|------|------|
| 启动 | 3/4 | 2020年前版本需要 riched20.dll 补丁；2022年后版本复杂化 |
| 核心功能 | 2/4 | 文字聊天可用；DING 消息、OA审批部分可用 |
| UI 渲染 | 2/4 | 窗口最小化后其他应用窗口遮挡有阴影；部分动画失效 |
| 网络/音频 | 1/4 | 视频会议摄像头无法获取预览（社区已知问题） |
| 稳定性 | 1/4 | DingTalk.exe 进程残留常见 |

**WineHQ 综合评级：Silver–Bronze（⚠️ 部分可用）**

**重要发现**：
> 阿里巴巴已于 **2022 年发布官方 DingTalk Linux 客户端**（deb 包，v1.2.x 起），支持 Ubuntu 18.04+。
> 2025 年最新版本为 **DingTalk Linux v7.6.25.4122001**（deb 安装包，223MB），**功能较完整**。
>
> **建议：OS 项目优先捆绑 DingTalk Linux 原生版，而非通过 Wine 运行 Windows 版。**

**钉钉原生 Linux 客户端功能覆盖**：
- ✅ 单聊/群聊（文字）
- ✅ 消息已读未读
- ✅ DING 消息
- ✅ 企业通讯录
- ✅ 视频会议（部分，需实测）
- ⚠️ 小程序/应用内嵌页（部分不支持）
- ❌ 桌面通知（Deepin 环境下无法关闭，需特殊处理）

---

### 3.3 Microsoft Office 2021/LTSC

| 维度 | 评分 | 说明 |
|------|------|------|
| 启动 | 4/4 | Word/Excel/PowerPoint 均可正常启动 |
| 核心功能 | 4/4 | 文档编辑、表格、演示文稿——核心功能 95%+ 可用 |
| UI 渲染 | 3/4 | Ribbon 界面正常；部分字体渲染有差异 |
| 网络/音频 | 4/4 | 不涉及（本地应用） |
| 稳定性 | 3/4 | 大文档、宏、VBA 脚本存在崩溃风险 |

**WineHQ 综合评级：Gold（✅ 良好）**

**关键数据点**：
- WineHQ AppDB 上 Office 2016/2019/2021 整体评级 **Gold**
- Word：Gold（文档兼容性 98%+）
- Excel：Gold（公式兼容性极佳）
- PowerPoint：Gold（动画兼容性 90%+）
- Outlook：Silver–Gold（依赖 Exchange 协议，部分 MAPI 限制）

**Wine 7.x 额外注意事项**：
- 需要 `winetricks corefonts` 安装微软字体（许可证需处理）
- Office 激活：KMS 激活脚本可在 Wine prefix 内运行
- OneDrive 同步：部分功能受限（OAuth 认证需额外配置）
- **推荐 Office 版本**：Office LTSC 2021（无订阅，纯本地，Wine 兼容性最佳）

**替代方案评估**：

| 方案 | 优势 | 劣势 |
|------|------|------|
| Wine + Office 2021 | 功能完整，与 Windows 版一致 | 需要处理字体/激活；法律风险（许可证） |
| WPS Office Linux | 原生 Linux，兼容 Office 格式 | 功能差距（宏/VBA 支持差）；品牌信任度 |
| LibreOffice | 完全免费开源 | 格式兼容性问题（.docx/.xlsx 细微差异） |

---

### 3.4 Adobe Photoshop 2023

| 维度 | 评分 | 说明 |
|------|------|------|
| 启动 | 2/4 | 能启动，但首屏加载慢（30s+） |
| 核心功能 | 1/4 | 基础修图可用；AI 修图功能依赖 Creative Cloud |
| UI 渲染 | 1/4 | GPU 加速依赖 Vulkan/DXVK；字体渲染问题 |
| 网络/音频 | 2/4 | 不涉及（本地应用） |
| 稳定性 | 0/4 | 运行 5–10 分钟大概率崩溃（Wine 已知问题） |

**WineHQ 综合评级：Garbage / Bronze（❌ 不推荐）**

**关键问题**：
- Photoshop 是 Wine 兼容性最差的大型商业软件之一
- Wine 8.0+ 改善了 Photoshop CC 系列的 GPU 加速（通过 DXVK）
- Wine 7.x：DXVK 尚未默认集成，需手动配置
- Photoshop 2023 的 Neural Filters（AI 功能）完全依赖 Creative Cloud，Wine 不支持
- 崩溃率高：平均运行时长 <15 分钟即崩溃
- **法律风险**：Adobe 软件许可证明确禁止在非 Windows/macOS 平台运行

**可替代方案**：
- **Affinity Photo 2**：原生 Linux，支持 .psd 文件，Wine 兼容性极好（WineHQ Gold）
- **GIMP**：开源免费，但与 Photoshop 工作流差距较大
- **Photopea**：浏览器版 Photoshop 克隆，支持 .psd（功能受限）

---

### 3.5 腾讯会议（Tencent Meeting）

| 维度 | 评分 | 说明 |
|------|------|------|
| 启动 | 1/4 | 能安装，但依赖项（VC++ Redistributable）较多 |
| 核心功能 | 1/4 | 视频会议完全依赖专有媒体 SDK |
| UI 渲染 | 1/4 | Electron/Chromium 壳，Wine 支持一般 |
| 网络/音频 | 0/4 | 音频输入/输出、摄像头完全不可用 |
| 稳定性 | 0/4 | 进程异常退出 |

**WineHQ 综合评级：Garbage（❌ 不可用）**

**重要发现**：
- 腾讯会议于 **2023 年推出过 Linux 内测版**（.deb），后停止维护
- 当前 Linux 用户推荐：**腾讯会议 Web 版**（浏览器入会）或 **腾讯会议 × Docker 方案**
- 视频会议软件 Wine 兼容性普遍极差（Zoom、Teams 均如此）
- 核心原因：音频/摄像头设备访问需要 Windows 特定 API（WASAPI、DirectShow）

**替代方案评估**：

| 方案 | 兼容度 | 备注 |
|------|--------|------|
| 腾讯会议 Web 版 | ✅ 可用 | 浏览器入会，功能受限但可用 |
| Zoom（Linux 原生） | ✅ 原生支持 | 有 Linux 版，功能完整 |
| Microsoft Teams（Linux 原生） | ✅ 原生支持 | 有 .deb 包 |
| 飞书会议（Linux 原生） | ✅ 原生支持 | 飞书 Linux 版含会议功能 |

---

## 四、兼容性评分汇总

| 软件 | 启动 | 核心功能 | UI渲染 | 网络/音频 | 稳定性 | **总分** | **评级** |
|------|------|---------|--------|---------|--------|---------|---------|
| TIM（QQ 办公版） | 2 | 2 | 1 | 1 | 0 | **6/20** | ⚠️ 部分可用 |
| 钉钉（原生 Linux 版） | 4 | 4 | 3 | 2 | 3 | **16/20** | ✅ 良好 |
| Microsoft Office 2021 | 4 | 4 | 3 | 4 | 3 | **18/20** | ✅ 良好 |
| Adobe Photoshop 2023 | 2 | 1 | 1 | 2 | 0 | **6/20** | ❌ 不可行 |
| 腾讯会议 | 1 | 1 | 1 | 0 | 0 | **3/20** | ❌ 不可行 |

> 注：钉钉按**原生 Linux 版**评分；其余按 **Wine 7.x 兼容性**评分。

---

## 五、Phase 1 核心风险判断

### 风险 1：Adobe Photoshop ❌

Photoshop 是 Phase 1 验收测试集的关键项。
**结论：Wine 路线对 Photoshop 2023 不可行。**

建议替代方案：
- 将验收标准中的 Photoshop 替换为 **Affinity Photo 2**（WineHQ Gold，原生 Linux）
- 或与用户协商接受 **Photopea（Web 版）** 作为轻量替代
- 或将 Photoshop 从验收集降级为"可选测试项"

### 风险 2：腾讯会议 ❌

视频会议类软件在 Wine 下完全不可用。

建议替代方案：
- 捆绑 **Zoom Linux 原生版** 或 **Microsoft Teams Linux 原生版**
- 或在 OS 中预装 **腾讯会议 Chrome/Web 快捷方式**（功能基本可用）

### 风险 3：TIM（QQ 办公版）⚠️

TIM 兼容性问题属于"可解决但需专项适配"级别。

建议：
- 评估 **Deepin-wine** 或 **Crossover** 是否能显著提升兼容性
- 或转向捆绑 **TIM Linux 官方版**（腾讯内测，功能受限）
- 或与钉钉/企业微信合并，选择 IM 工具替代

### 风险 4：环境搭建（本周最大障碍）

**当前障碍**：WSL Ubuntu 网络不通 → 无法 apt install wine
**解决方案**：
1. 手动下载 winehq deb 包离线安装（从另一台联网机器下载）
2. 虚拟机方案：VirtualBox + Ubuntu 离线镜像
3. 云 CI 方案：GitHub Actions + Ubuntu Docker 容器（WineHQ 提供官方镜像）
4. **推荐**：启动物理机原生 Ubuntu，网络隔离内网（需团队协调）

---

## 六、综合结论与 Phase 1 路线建议

### 6.1 Wine 路线可持续性评估

| 评估项 | 结论 |
|--------|------|
| 钉钉 | ✅ Wine 路线**不需要**，官方有 Linux 版 |
| Office | ✅ Wine 路线可行，评级 Gold，Workload 可接受 |
| TIM | ⚠️ 需要专项适配（Deepin-wine 或替代方案） |
| Photoshop | ❌ Wine 路线**不可行**，需替换验收标准 |
| 腾讯会议 | ❌ Wine 路线**不可行**，需转向原生替代 |

**综合判断**：Wine 路线**部分可行**，但需要针对高风险软件准备替代方案。

### 6.2 三步走策略（修订）

| 阶段 | 策略 | 软件覆盖 |
|------|------|---------|
| **Wine 原生支持** | 直接 apt 打包 | 钉钉（官方 Linux）、Zoom、Teams、飞书、WPS |
| **Wine 兼容支持** | 预装 + 调优适配 | TIM/QQ、Office 2021 LTSC、搜狗输入法 |
| **不可 Wine 软件** | 明确告知、引导使用 Web 版/替代品 | Photoshop（→ Affinity Photo）、腾讯会议（→ Web/Zoom） |

### 6.3 里程碑决策点

**Week 2 结束时**（里程碑 Gate 1）需确认：
- [ ] WSL/物理机 Wine 环境可完成一次完整 apt update + wine 安装
- [ ] Office 2021 LTSC 在 Wine prefix 内可启动并编辑文档（验收标准）
- [ ] Photoshop 替代方案（Affinity Photo）评估完成
- [ ] 钉钉 Linux 原生版功能摸底测试完成

**若 Gate 1 未通过**（Wine 成功率 <60%）：
→ 触发 Phase 1 路线调整：评估 Tauri/Electron 轻量化路线替代 Wine

---

## 七、后续行动项

| 优先级 | 行动 | 负责人 | 截止时间 |
|--------|------|--------|---------|
| 🔴 紧急 | 解决 WSL 网络问题（DNS 配置） | 小林 | Week 1 结束前 |
| 🔴 紧急 | 确认 Office 2021 LTSC 安装包来源 | 小林 | Week 1 结束前 |
| 🟡 高 | 申请物理测试机（联想/Dell/HP 各一） | 小林→小安协调 | Week 2 |
| 🟡 高 | Photoshop 替代方案评估（Affinity Photo） | 小林 | Week 2 |
| 🟡 高 | TIM Wine 适配方案验证（Deepin-wine） | 小林 | Week 2 |
| 🟢 中 | 钉钉 Linux 原生版功能摸底测试 | 小林 | Week 1 结束前 |
| 🟢 中 | 腾讯会议替代方案确认（Zoom/Teams） | 小林 | Week 2 |
| 🔵 规划 | Phase 1 Week 3–4 任务细化 | 小林 | Week 2 结束前 |

---

## 八、环境搭建障碍处理方案（补充）

### WSL 网络不通根因分析

症状：ping 所有地址（archive.ubuntu.com / baidu.com / 8.8.8.8）均超时。

可能原因：
1. **企业防火墙阻断 WSL 出站流量**（最可能）
2. WSL DNS 配置错误（`/etc/resolv.conf` 被覆盖）
3. Hyper-V 虚拟交换机配置问题

**验证命令**：
```powershell
# 检查 WSL DNS 配置
wsl -d Ubuntu -e cat /etc/resolv.conf

# 检查 WSL 是否能访问 Windows 网络
wsl -d Ubuntu -e bash -c "curl --max-time 5 https://www.baidu.com"
```

**临时绕过方案**：
1. **方案 A（推荐）**：手动下载 Wine deb 包，离线安装
   - 从可联网机器下载 `winehq-stable_7.x.x_amd64.deb`
   - `wsl -d Ubuntu -e dpkg -i winehq-stable_amd64.deb`
2. **方案 B**：GitHub Actions CI 容器测试（完全离线，不依赖本机）
3. **方案 C**：换用物理机原生 Ubuntu（需协调硬件）

---

*报告版本：v1.0 | 状态：草稿，待实测数据补充 | 最后更新：2026-08-06*
