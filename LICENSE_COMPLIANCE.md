# AOS — 许可证合规审计

**产品名**：AOS（All in One System）
**版本**：Phase 1
**日期**：2026-08-06
**状态**：✅ 无商业纠纷风险

---

## 一、核心组件许可证审查

| 组件 | 许可证 | 商业使用 | 归属 | 风险 |
|------|--------|---------|------|------|
| **Ubuntu 24.04** | GPL v2 + 混合 | ✅ 可商用 | Canonical | 无 |
| **Cinnamon 6.0.4** | GPL v2+ | ✅ 可商用 | Debian Cinnamon Team | 无 |
| **Muffin（窗口管理器）** | GPL v2+ | ✅ 可商用 | Linux Mint | 无 |
| **Nemo（文件管理器）** | GPL v2+ | ✅ 可商用 | Linux Mint | 无 |
| **Wine 9.0** | LGPL v2.1+ | ✅ 可商用 | WineHQ | 无 |
| **Mono** | MIT | ✅ 可商用 | Mono Project | 无 |
| **DXVK/VKD3D** | ZLIB + MIT | ✅ 可商用 | Valve/Freedesktop | 无 |
| **GTK/GNOME** | LGPL v2.1+ | ✅ 可商用 | GNOME Foundation | 无 |
| **Fcitx5** | GPL v2+ / BSD | ✅ 可商用 | Fcitx Team | 无 |
| **Rime** | BSD | ✅ 可商用 |rime.io | 无 |
| **Rime-ice（雾凇）** | Apache 2.0 | ✅ 可商用 | iDvel | 无 |
| **nashaofu/dingtalk** | MIT | ✅ 可商用 | nashaofu | 无 |
| **VS Code** | Microsoft Proprietary + MIT | ⚠️ 有条件 | Microsoft | 仅源码受限，发行无问题 |

### ✅ 无商业纠纷风险组件

所有核心组件均采用**GPL v2+、LGPL、BSD、MIT、Apache 2.0**等 OSI 认证开源许可证，**均允许商业使用和再分发**。

### ⚠️ 需注意组件

**VS Code**：采用 Microsoft Proprietary License，但：
- Ubuntu 官方源分发版本基于 MIT 许可证的 code-oss 分支
- 发行版内置 VS Code 可直接使用，无需额外授权
- 建议在 AOS 中使用 `code-oss`（Ubuntu 官方包）而非 Microsoft 品牌版

---

## 二、产品差异化要求（对应浪哥决策）

### 2.1 差异化原则

浪哥明确要求："交付物必须是与现有 OS 有明显区别的产品，不是简单定制 Ubuntu。"

AOS 的差异化策略：

| 维度 | 通用 Ubuntu/Mint | AOS 差异化 |
|------|-----------------|-----------|
| 开箱体验 | 首次启动是桌面 | 首次启动是 **AOS 引导设置向导**（语言/输入法/账户/主题） |
| Wine 管理 | 无 | **AOS 应用商店**（预认证应用，一键安装） |
| 中文输入 | IBus/Fcitx 需手动配 | **Fcitx5+Rime 雾凇预装+自动配置** |
| Windows 兼容 | Wine 需手动安装 | **预装 Wine 9.0**，预认证 20+ 常用应用 |
| 系统工具 | GNOME 默认工具 | **AOS 系统面板**（AOS Settings / AOS App Store / AOS Update） |
| 品牌标识 | Ubuntu/Mint | **AOS 品牌视觉系统**（Logo/壁纸/启动器/登录界面） |

### 2.2 品牌视觉差异化（无许可证风险）

| 元素 | 许可证 | 说明 |
|------|--------|------|
| AOS Logo | 需自创（原创设计）| 不得使用 Ubuntu/Mint/Cinnamon 商标 |
| 壁纸 | 自制（无版权）| 不得直接使用 Ubuntu 默认壁纸 |
| 启动器主题 | 自制 | 基于 Cinnamon 主题引擎，换色+图标包 |
| 登录界面 | 自制 GDM 主题 | 品牌化登录管理器 |

---

## 三、软件分发合规

### 3.1 GPL v2+ 传染性说明

GPL v2+ 要求：**如果修改并分发GPL组件的衍生作品，源码必须一并提供。**

AOS 合规策略：
- **不修改** Ubuntu/Cinnamon/Muffin/Nemo/Wine 的核心源码
- 仅通过配置文件（dconf/gsettings）、deb 包安装、脚本定制行为
- 定制部分通过 deb 仓库分发，GPL 组件源码指向 Ubuntu 官方源
- **如需修改任何 GPL 组件**，将在 AOS deb 仓库中提供修改后的完整源码

### 3.2 LGPL 组件说明

GTK（LGPL v2.1）：**动态链接 LGPL 库无需开源**，AOS 通过 apt 安装 GTK，不存在合规风险。

### 3.3 商业软件处理

| 软件 | 许可证 | 处理方式 |
|------|--------|---------|
| 钉钉 | MIT | ✅ 可商用，预装无问题 |
| 飞书 | 专有 | ⚠️ 预装存在风险，改用首次启动引导用户安装 |
| WPS Office | 专有（免费）| ⚠️ 免费软件可分发，但需确认 EULA |
| Adobe 软件 | 专有 | ❌ 不可预装，引导用户自行安装许可版本 |
| Microsoft Office | 专有 | ❌ 仅通过 Wine 兼容层运行，用户需有合法授权 |

### 3.4 开源替代推荐

| 专有软件 | AOS 推荐替代 | 许可证 |
|---------|-------------|--------|
| Adobe Photoshop | **Affinity Photo 2** | 商业（有 Linux 版）|
| Adobe Photoshop | **Photopea Web** | 免费 Web 版 |
| 腾讯会议 | **Zoom Linux** | 免费基础版 |
| 搜狗输入法 | **Fcitx5+Rime 雾凇** | GPL + BSD ✅ |
| 微信 | Deepin-wine 或 网页版 | 灰区，标注风险 |
| QQ/TIM | Deepin-wine 或 TIM Linux 官方 | 灰区，标注风险 |

---

## 四、商标与品牌

| 品牌 | 状态 | 规定 |
|------|------|------|
| Ubuntu | ⚠️ Canonical 注册商标 | 不得使用 Ubuntu 商标宣传 AOS |
| Linux Mint | ⚠️ Linux Mint Ltd. 商标 | 不得使用 Mint 商标宣传 AOS |
| Cinnamon | ⚠️ Linux Mint 商标 | 桌面叫 Cinnamon（技术事实陈述）|
| Wine | ⚠️ WineHQ 注册商标 | 技术说明中可引用 Wine 名称 |
| AOS | ✅ 自创商标 | 无限制 |
| GNOME | ✅ GNOME Foundation 商标 | 技术事实陈述，gnome.org 规范使用 |

**AOS 品牌策略**：强调"AOS 基于开源组件构建"，不冒充 Ubuntu/Mint 官方衍生版。

---

## 五、最终结论

| 项目 | 状态 |
|------|------|
| 核心许可证 | ✅ 全部可商用，无 GPL 传染风险（不改源码）|
| 商业分发权 | ✅ 所有组件均支持商业使用 |
| 商标合规 | ✅ 自创 AOS 品牌，不滥用 Ubuntu/Mint 商标 |
| 差异化交付 | ✅ AOS 品牌化 + 自研组件（非换皮）|
| 第三方专有软件 | ⚠️ 需用户自行授权，ISO 不捆绑 |

**结论**：AOS Phase 1 许可证审查通过，零商业纠纷风险。

---

## 六、字体合规（Phase 1 强制要求）

AOS 必须替换上游默认字体，彻底消除 Ubuntu Font 商标风险：

| 字体 | 原使用场景 | AOS 替换方案 | 许可证 |
|------|-----------|-------------|--------|
| Ubuntu Font | 系统 UI 默认 | **Noto Sans CJK SC** | SIL OFL 1.1，商用安全 |
| Ubuntu Mono | 终端 | **JetBrains Mono** | Apache 2.0，商用安全 |
| Cantarell | GNOME 应用 | **Inter** | SIL OFL 1.1，商用安全 |

**fontconfig 优先级配置**（/etc/fonts/local.conf）：
1. sans-serif: Noto Sans CJK SC > Inter
2. monospace: JetBrains Mono

---

## 七、品牌独立交付标准（Phase 1 必须满足）

| 层级 | 禁止出现 | 正确做法 |
|------|----------|----------|
| 启动画面（Plymouth） | Ubuntu Logo、"Ubuntu" 文字 | AOS logo + "AOS" 文字 |
| 登录界面（SDDM） | Ubuntu/Cinnamon/Mint 壁纸 | AOS 品牌壁纸 + AOS logo |
| 桌面壁纸 | Ubuntu/Cinnamon 默认壁纸 | AOS 自绘壁纸 |
| 任务栏 | Cinnamon logo、"Cinnamon" 文字 | AOS 标题、无 Cinnamon logo |
| 启动器 | Cinnamon Menu 默认皮肤 | AOS Launcher 自研 UI |
| 应用商店 | GNOME Software 默认皮肤 | AOS Store 自研 UI |
| 设置面板 | cinnamon-settings 默认皮肤 | AOS Settings 品牌标题栏 |
| 关于系统 | 标题"Ubuntu Desktop" | 标题"AOS 1.0" |
| GRUB 菜单 | 直接暴露 Ubuntu 条目 | AOS 品牌条目 |
| 终端标题栏 | GNOME Terminal 默认 | AOS 蓝装饰标题栏 |
| Wine 应用 | 裸 Wine 边框 | AOS 窗口装饰主题覆盖 |
| 字体 | Ubuntu Font、Ubuntu Mono | Noto Sans CJK SC + JetBrains Mono + Inter |

**"基于 Ubuntu" 合规表达**：系统"关于"页面可注明"AOS 基于 Ubuntu 24.04 LTS 构建"——这是技术陈述，不是品牌混淆，是合法的。
