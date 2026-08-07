# AOS 品牌规范 v1.0

> **执行原则**：AOS 是独立桌面操作系统，不是 Ubuntu/Cinnamon 换皮。所有用户可见界面必须承载 AOS 品牌，与上游发行版视觉脱钩。

---

## 一、品牌标识体系

### 1.1 系统名称
| 场合 | 展示名称 |
|------|----------|
| 启动画面（Plymouth） | **AOS** |
| 桌面环境标题栏 | **AOS Desktop** |
| 任务栏 | **AOS Taskbar** |
| 登录界面（SDDM/GDM） | **AOS** |
| 终端提示符 | `aos@aos:~$` |
| 系统设置面板标题 | **AOS 设置** |
| 应用商店 | **AOS Store** |
| 关于系统 | **AOS 1.0** |

**禁止出现**：Ubuntu、Cinnamon、Linux Mint、GNOME Desktop 字样（设置面板"关于"里可以注明底层基于 Ubuntu 24.04）

### 1.2 视觉标识

#### Logo
- **主 Logo**：AOS 文字徽标（SVG，浅色/深色两个版本）
- **来源**：自绘，零第三方版权
- **替代**：如果自绘困难，使用无版权几何图形（自制），禁止使用 Ubuntu 圆盘 logo、Cinnamon 糖块 logo、Mint 叶片 logo

#### 壁纸
- **默认壁纸**：AOS 品牌定制（1920×1080 + 2560×1440）
- **来源**：自绘或 CC0/CC-BY 授权图片
- **禁止**：Ubuntu 默认壁纸（ubuntu-logo.svg）、Cinnamon 默认壁纸

#### 图标主题
- **使用**：Papirus（LGPL，可商用）或自研 AOS 图标集
- **禁止**：Ubuntu Yunuo/Ubuntu-mono-* 图标集
- **如用 Papirus**：在 `LICENSE_COMPLIANCE.md` 中注明并附 GPL 兼容声明

#### 色彩体系
| 角色 | 色值 | 用途 |
|------|------|------|
| 主色 | `#1A73E8`（AOS 蓝） | 强调、按钮、选中态 |
| 辅色 | `#34D399`（AOS 绿） | 成功状态、进度条 |
| 背景 | `#1E1E2E`（深色）/ `#F5F5F5`（浅色） | 桌面背景、面板 |
| 文字 | `#FFFFFF` / `#1F1F1F` | 对应主题 |

---

## 二、自研组件要求（Phase 1 必须交付）

### 2.1 AOS Launcher（启动器）
- **替代**：Cinnamon 菜单 → AOS 启动器
- **要求**：左侧应用分类 + 搜索框 + 快捷方式，视觉与 Cinnamon Menu 完全区分
- **技术选型**：Python3 + GTK4 或 Qt6，界面自行设计
- **禁止**：直接使用 cinnamon-menu 的默认皮肤

### 2.2 AOS Store（应用商店）
- **要求**：自有 UI 设计，列出预装 deb 应用，支持 apt install 触发
- **禁止**：直接暴露 Software（GNOME）或 cinnamon-software 的默认皮肤
- **技术选型**：Vala/GTK4 或 Flutter（推荐 Flutter，跨平台扩展预留）
- **Phase 1 交付**：仅展示预装应用列表 + 安装按钮（钉钉/Office兼容层等）

### 2.3 AOS 设置面板
- **替代**：cinnamon-settings → AOS 设置
- **要求**：品牌标题栏 + AOS 蓝强调色
- **禁止**：直接使用 cinnamon-settings-daemon 的默认皮肤
- **Phase 1 交付**：网络/显示/输入法/关于，四大核心面板

### 2.4 AOS 主题
- **窗口装饰**：mutter/nemo 主题使用 AOS 定制配色（AOS 蓝标题栏）
- ** Plymouth**：启动 splash 显示 AOS logo + 进度条（禁止 Ubuntu 文字）
- **SDDM**：登录界面全屏 AOS 品牌壁纸 + AOS logo（禁止 Ubuntu 桌面背景）
- **GRUB**：启动菜单添加 AOS 条目，移除 Ubuntu 标识

---

## 三、Wine 层隔离要求

### 3.1 用户不可见 Wine 原始界面
- Windows 应用通过 AOS App Runner 启动，不直接暴露 Wine 进程
- Wine 应用窗口标题栏显示 AOS 品牌装饰（AOS 边框/按钮）
- Wine 应用开始菜单入口：通过 AOS Launcher 的 "Windows 应用" 分类，不暴露原始 Wine 菜单

### 3.2 Wine 配置隐藏
- `WINEPREFIX` 环境变量自动设置，用户无感知
- Wine 配置工具（winecfg）不暴露给普通用户，仅开发者调试用
- `~/.wine` 目录权限 700，不在文件管理器直接显示

---

## 四、许可证清理清单

### 4.1 商标（Trademark）
| 项目 | 来源 | 合规状态 |
|------|------|----------|
| Ubuntu | Canonical 商标 | ⚠️ ISO 启动画面/GRUB/ Plymouth 不得出现 Ubuntu 品牌；"基于 Ubuntu" 可在系统设置"关于"中注明 |
| GNOME | GNOME Foundation 商标 | ⚠️ 桌面环境底层是 Cinnamon，但仍基于 GNOME 技术栈；设置"关于"可注明 |
| Cinnamon | Linux Mint 商标 | ⚠️ 代码层面使用 Cinnamon 库，但启动器/主题/壁纸必须 AOS 品牌 |
| Wine | WineHQ 商标 | ✅ Wine 是开源项目（非商标注册），HP 公司对"Hewlett-Packard"类商标有不同规则；Wine 本身无注册商标限制 |
| Linux | Linus Torvalds 商标 | ✅ "Powered by Linux" 在系统"关于"页面合法使用（社区许可） |

### 4.2 字体
| 字体 | 许可证 | 使用场景 | 合规 |
|------|--------|----------|------|
| Ubuntu Font | Ubuntu Font License 1.0 | 系统默认 UI 字体 | ⚠️ 可内置但需注明来源；推荐替换为 Noto Sans CJK SC（SIL OFL，可商用） |
| Noto Sans CJK SC | SIL Open Font License 1.1 | 中文字体 | ✅ SIL OFL，商用安全 |
| JetBrains Mono | Apache 2.0 | 终端字体 | ✅ 商用安全 |
| Inter | SIL Open Font License 1.1 | 西文字体 | ✅ 商用安全 |

**决策**：UI 字体统一用 **Noto Sans CJK SC + Inter**，零版权风险。

### 4.3 软件包许可证
所有 apt 安装包在 ISO 发布前必须通过 `packages.linuxmint.com/licence.php` 类似清单或 `/license` 文件核查。

Phase 1 预装软件许可证策略：
- **系统层**（apt 标准包）：GPL/LGPL/BSD/MIT，商用安全
- **Wine**：LGPL 2.1
- **Fcitx5+Rime**：GPL + BSD
- **钉钉**：MIT
- **Cinnamon**：GPL（Linux Mint 主导，LGPL 协议文件）

---

## 五、品牌开发任务（Phase 1 拆分）

### Week 4-5：品牌素材制作
- [ ] AOS Logo 设计（SVG，浅/深色版）
- [ ] 默认壁纸制作（1920×1080 + 2560×1440）
- [ ] Plymouth 主题（启动 splash）
- [ ] SDDM 登录界面主题
- [ ] GRUB 品牌条目
- [ ] 窗口装饰主题（AOS 蓝标题栏）

### Week 6-7：自研启动器
- [ ] AOS Launcher UI 设计
- [ ] Python/GTK4 或 Qt6 实现
- [ ] 应用分类逻辑（系统/办公/网络/工具/Windows 应用）
- [ ] 搜索功能

### Week 8-9：自研设置面板
- [ ] AOS 设置 UI（GTK4/Qt）
- [ ] 网络设置面板
- [ ] 显示设置面板
- [ ] 输入法配置面板（集成 Fcitx5-Rime）
- [ ] 关于 AOS 面板（注明基于 Ubuntu 24.04）

### Week 10-12：自研应用商店
- [ ] AOS Store UI 设计
- [ ] apt 包列表读取（dpkg -l 解析）
- [ ] deb 安装触发器
- [ ] Phase 1 交付：钉钉 + 预装应用入口

---

## 六、ISO 发布前品牌核查清单

在 AOS v0.1 发布前必须逐项确认：

- [ ] 启动画面（Plymouth）：无 Ubuntu Logo，无 "Ubuntu" 文字
- [ ] 登录界面（SDDM）：无 Ubuntu/Cinnamon/Mint 壁纸
- [ ] 桌面壁纸：非 Ubuntu/Cinnamon 默认壁纸
- [ ] 任务栏/面板：标题显示 "AOS"，无 Cinnamon logo
- [ ] 开始菜单/Launcher：品牌定制 UI，非 Cinnamon 默认
- [ ] 应用商店：品牌定制 UI
- [ ] 设置面板：品牌定制 UI，标题栏 "AOS 设置"
- [ ] 关于系统：显示 "AOS 1.0"，可注明基于 Ubuntu 24.04（注明 ≠ 品牌混淆）
- [ ] 字体：已替换为 Noto Sans CJK SC + Inter，无 Ubuntu Font
- [ ] GRUB 菜单：AOS 条目存在，无 Ubuntu 标识
- [ ] 终端窗口标题：AOS 品牌标题栏装饰

---

*本文档是 AOS Phase 1 品牌规范的权威来源。Phase 1 所有交付物必须符合本规范要求。*
