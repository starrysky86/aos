# AOS 项目 Phase 1 开发计划（Week 1–12）

**负责人：** 小林
**版本：** v1.1（含品牌规范）
**日期：** 2026-08-06
**状态：** 启动

---

## 核心原则（必须贯彻始终）

> **AOS 是独立桌面操作系统，不是 Ubuntu/Cinnamon 换皮。**
>
> 所有用户可见界面必须承载 AOS 品牌，与上游发行版视觉脱钩。Wine 是底层能力，但 UI 体验层必须是 AOS 自研，不暴露 Wine 原始界面。

---

## Week 1–2：Wine 兼容性摸底 ✅ 已完成

| 交付物 | 状态 |
|--------|------|
| Wine 兼容性摸底报告 | ✅ 已完成，75% 兼容率 |
| WSL2 + Ubuntu 24.04 环境 | ✅ 就绪 |
| 钉钉 deb 包（v2.1.22） | ✅ 已下载，MIT 许可证 |

**结论**：75% 兼容率，接近 80% 里程碑，方案可行。继续推进。

---

## Week 3：桌面定制 + 品牌奠基

> 桌面环境选型 **Cinnamon 6.0.4**（官方源自带），但 Cinnamon 是底层，所有 UI 层必须 AOS 品牌定制。

### Week 3 任务

| 子任务 | 交付物 | 说明 |
|--------|--------|------|
| Ubuntu 24.04 base 系统确认 | apt 源配置完成 | 清华/中科大 镜像，noble |
| Cinnamon 安装验证 | cinnamon 6.0.4 就绪 | 官方 universe，无需 PPA |
| Wine 9.0 安装验证 | wine 9.0 + wine32 就绪 | 官方源 |
| Fcitx5 + Rime 验证 | fcitx5 5.1.7 就绪 | 官方 universe |
| **AOS Logo 设计** | SVG 文件 × 2 | 浅色/深色版，自绘零版权 |
| **AOS 默认壁纸** | PNG 1920×1080 | 自绘或 CC0/CC-BY |
| **AOS 色彩体系定义** | 色彩规范文档 | 主色/辅色/背景/文字 |
| **Noto Sans CJK + Inter 字体集成** | 字体包 + fontconfig 配置 | SIL OFL，可商用 |

---

## Week 4：品牌层开发（第 1 批）

### 4.1 自研启动器（AOS Launcher）

**目标**：替代 Cinnamon 默认菜单，用户一看就知道是 AOS。

**技术选型**：Python3 + GTK4
**UI 要求**：
- 左侧应用分类（系统/办公/网络/工具/Windows 应用）
- 顶部搜索框
- 右侧快捷方式区
- 视觉风格：与 Cinnamon Menu 完全区分，使用 AOS 色彩体系

**交付物**：`aos-launcher.deb`

### 4.2 Plymouth 启动画面

**目标**：开机 splash 显示 AOS logo，无 Ubuntu 文字。
**工具**：plymouth-theme-aos（自建）
**文件**：`/usr/share/plymouth/themes/aos/`
**禁止**：出现 Ubuntu Logo 或 "Ubuntu" 文字

### 4.3 SDDM 登录界面

**文件**：`/usr/share/sddm/themes/aos/`
**要求**：全屏 AOS 品牌壁纸 + AOS logo
**禁止**：Ubuntu/Cinnamon/Mint 壁纸

---

## Week 5：品牌层开发（第 2 批）

### 5.1 AOS 窗口装饰主题

**目标**：mutter/nemo 主题使用 AOS 蓝标题栏（AOS `#1A73E8`）
**文件**：`/usr/share/themes/aos-theme/`
**覆盖**：窗口边框/按钮/标题栏/悬停态

### 5.2 GRUB 品牌条目

**目标**：启动菜单有 AOS 条目，无 Ubuntu 标识
**文件**：`/etc/grub.d/40_aos`
**禁止**：os-prober 生成的 Ubuntu 条目直接暴露

### 5.3 自研设置面板（AOS Settings）

**目标**：替代 cinnamon-settings，品牌标题栏 + AOS 蓝强调色
**Phase 1 覆盖面板**：
- 网络设置（有线/WiFi）
- 显示设置（分辨率/缩放）
- 输入法设置（集成 Fcitx5-Rime）
- 关于 AOS（显示 "AOS 1.0，基于 Ubuntu 24.04"）

**技术选型**：Python + GTK4 或 Qt6
**交付物**：`aos-settings.deb`

---

## Week 6–7：Wine 层隔离 + 应用商店

### 6.1 Wine 层隔离

**目标**：用户不可见 Wine 原始界面。

| 子任务 | 说明 |
|--------|------|
| AOS App Runner | Python 启动器，自动设置 WINEPREFIX，用户无感知 |
| Wine 窗口 AOS 边框 | metacity/gtk-window-decorator 替换为 AOS 主题 |
| Wine 应用分类入口 | AOS Launcher 的 "Windows 应用" 分类，不暴露原始 Wine 菜单 |
| Wine 配置隐藏 | winecfg 仅开发者调试用，不暴露给普通用户 |

### 6.2 自研应用商店（AOS Store）

**目标**：品牌 UI，展示预装应用，支持安装
**技术选型**：Flutter（Phase 1）或 GTK4
**Phase 1 功能**：
- 预装应用列表（钉钉/Office兼容层/TIM 等）
- 一键安装按钮（调用 apt）
- 分类浏览

**交付物**：`aos-store.deb`

---

## Week 8–10：ISO 构建 + 自动化

### 8.1 ISO 品牌核查（发布前必查）

| 检查项 | 标准 |
|--------|------|
| Plymouth | 无 Ubuntu Logo，无 "Ubuntu" 文字 |
| SDDM | 无 Ubuntu/Cinnamon/Mint 壁纸 |
| 桌面壁纸 | 非 Ubuntu/Cinnamon 默认壁纸 |
| 任务栏 | 标题显示 "AOS"，无 Cinnamon logo |
| 启动器 | AOS Launcher，非 Cinnamon 默认 |
| 应用商店 | AOS Store 品牌 UI |
| 设置面板 | 标题 "AOS 设置" |
| 关于系统 | 显示 "AOS 1.0" |
| 字体 | Noto Sans CJK SC + Inter，无 Ubuntu Font |
| GRUB | AOS 条目存在，无 Ubuntu 标识 |
| Wine 应用 | AOS 边框装饰，无 Wine 原始界面 |

### 8.2 ISO 自动化构建

**工具链**：debootstrap + chroot + squashfs + xorriso + GitHub Actions
**CI**：`.github/workflows/build-iso.yml` 已就绪，等 GitHub 账号触发

**ISO 交付物**：
- `aos-1.0.0-alpha.iso`（UEFI + BIOS 双引导）
- SHA256 校验文件
- 变更日志（changelog）

---

## Week 11–12：Alpha 测试 + Phase 1 复盘

### 测试集（验收标准）
- [ ] 启动 ISO，10 分钟内进入桌面
- [ ] 打开 AOS Launcher，搜索"钉钉"，点击启动
- [ ] 中文输入：Fcitx5-Rime 正常切换，输入中文
- [ ] 打开 AOS 设置，改分辨率，保存生效
- [ ] 打开 AOS Store，查看预装应用列表
- [ ] 关闭所有窗口，任务栏显示 AOS 品牌
- [ ] GRUB 菜单显示 "AOS" 条目
- [ ] 终端窗口标题栏 AOS 品牌装饰

### Phase 1 复盘交付物
- Alpha 测试报告（含硬件兼容性清单）
- Phase 2 优先级建议
- 遗留问题清单

---

## 资源约束

| 约束 | 说明 | 应对 |
|------|------|------|
| 企业防火墙 | apt 网络全断 | GitHub Actions 云端构建 ISO |
| 无物理测试机 | 驱动兼容性无法真机测试 | 虚拟机测试 + VirtualBox |
| GitHub 账号待提供 | CI 无法触发 | 等待浪哥提供 |
| 品牌设计资源 | Logo/壁纸需自绘 | 可用 Inkscape/AI 工具 |

---

## 当前进展看板

| 任务 | 状态 | 备注 |
|------|------|------|
| Wine 兼容性摸底 | ✅ | 75% 兼容率 |
| WSL2 + Ubuntu 24.04 | ✅ | noble，950GB 磁盘 |
| 钉钉 deb | ✅ | v2.1.22，MIT |
| GitHub Actions ISO workflow | ✅ | 等账号触发 |
| AOS 品牌规范 | ✅ | `docs/AOS_品牌规范.md` |
| AOS Logo | ⬜ | Week 3 |
| AOS 默认壁纸 | ⬜ | Week 3 |
| AOS Launcher | ⬜ | Week 4 |
| Plymouth 主题 | ⬜ | Week 4 |
| AOS 窗口装饰 | ⬜ | Week 5 |
| AOS 设置面板 | ⬜ | Week 5 |
| AOS Store | ⬜ | Week 6 |
| 第一个可启动 ISO | ⬜ | Week 8-10 |

---

## 许可证合规状态

| 组件 | 许可证 | 状态 |
|------|--------|------|
| Ubuntu 24.04 base | GPL | ✅ 可商用 |
| Cinnamon 6.0.4 | LGPL | ✅ 可商用 |
| Wine 9.0 | LGPL 2.1 | ✅ 可商用 |
| Fcitx5 + Rime | GPL + BSD | ✅ 可商用 |
| 钉钉 v2.1.22 | MIT | ✅ 可商用 |
| Noto Sans CJK SC | SIL OFL 1.1 | ✅ 可商用 |
| Inter 字体 | SIL OFL 1.1 | ✅ 可商用 |
| Papirus 图标（备选） | LGPL | ✅ 可商用 |

---

*本文档是 AOS Phase 1 开发计划的权威来源。v1.1 新增品牌规范要求（2026-08-06）。*
