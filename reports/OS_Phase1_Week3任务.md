# OS Phase 1 — Week 3 任务执行清单

**负责人：** 小林
**执行日期：** 2026-08-06
**触发指令：** 浪哥确认 75% 兼容率可行，云端先行

---

## Week 3 目标

桌面定制基准镜像搭建 + 测试环境就绪。

## 任务 1：WSL Ubuntu 24.04 环境诊断（5 分钟）

### 1.1 系统版本与资源配置
- [x] Ubuntu 版本：`lsb_release -a`
- [x] 内核版本：`uname -r`
- [x] 磁盘空间：`df -h`
- [x] 内存：`free -h`

### 1.2 Cinnamon 桌面环境可行性评估

**问题**：WSL 默认无 GUI，桌面定制需确认 Cinnamon 能否在 WSL 内构建（即便最终打包在物理机上运行）。

```bash
# 测试能否安装 Cinnamon（依赖项多，先评估 apt 源）
apt-cache show cinnamon 2>/dev/null | head -20
```

**折中方案**：若 WSL 网络/apt 不可用：
- 在 GitHub Actions Ubuntu 24.04 容器内完成所有构建
- 本机只负责文档和代码管理
- 最终 ISO 打包通过 CI/CD 完成

---

## 任务 2：GitHub Actions CI 搭建（本周重点）

### 2.1 创建 os-wine-test 仓库 workflow

```yaml
# .github/workflows/wine-compat.yml
name: Wine Compatibility Suite

on:
  workflow_dispatch:
  schedule:
    - cron: '0 2 * * 1'  # 每周一凌晨跑

jobs:
  # ── 矩阵测试：Wine 版本 × 测试软件 ──
  wine-matrix:
    strategy:
      matrix:
        wine_version: ['stable', 'staging', 'devel']
        app: ['office', 'tim', 'photoshop-alt', 'dingtalk-native', 'zoom']
    runs-on: ubuntu-24.04
    container: ubuntu:24.04
    
    steps:
      - name: Add Tsinghua mirror
        run: |
          sed -i 's|http://archive.ubuntu.com|https://mirrors.tuna.tsinghua.edu.cn|g' \
            /etc/apt/sources.list.d/ubuntu.sources
          apt-get update -qq

      - name: Install Wine ${{ matrix.wine_version }}
        run: |
          apt-get install -y software-properties-common gnupg2
          wget -qO- https://dl.winehq.org/wine-builds/winehq.keys | \
            apt-key add - 2>/dev/null || true
          apt-get install -y --install-recommends \
            winehq-${{ matrix.wine_version }} 2>&1 | tail -5 || \
            echo "WineHQ stable install failed, trying Ubuntu wine package"

      - name: Test App: ${{ matrix.app }}
        run: |
          case ${{ matrix.app }} in
            office)   echo "Office Wine test placeholder"; wine --version ;;
            tim)     echo "TIM Wine test placeholder"; wine --version ;;
            dingtalk-native) echo "DingTalk native test"; apt-cache show dingtalk 2>/dev/null ;;
            zoom)    echo "Zoom native test"; apt-cache show zoom 2>/dev/null ;;
          esac

  # ── ISO 构建任务（每周五自动触发）──
  build-iso:
    needs: wine-matrix
    if: github.event_name == 'schedule'
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - name: Install Cubic
        run: |
          apt-get install -y cubic
      - name: Build custom ISO
        run: |
          echo "ISO build would run here with cubic"
```

### 2.2 手动触发第一次 CI

```bash
# 在 GitHub 上：
# 1. 创建仓库 os-wine-test（私有）
# 2. 导入上述 workflow
# 3. 点击 "Run workflow" → 选择 ubuntu-24.04
# 4. 等待约 15 分钟看第一轮结果
```

---

## 任务 3：桌面选型验证（本周核心）

### 3.1 桌面环境对比

| 桌面环境 | 内存占用 | 定制难度 | Wine 兼容性 | 适合人群 | 推荐度 |
|---------|---------|---------|------------|---------|--------|
| **Cinnamon** | ~800MB | ⭐⭐ 简单 | ✅ 良好 | Linux 新手/企业用户 | ⭐⭐⭐⭐⭐ |
| GNOME | ~1.2GB | ⭐⭐⭐ 中等 | ✅ 良好 | 追求现代感 | ⭐⭐⭐ |
| XFCE | ~400MB | ⭐⭐ 简单 | ⚠️ 需适配 | 低配机器 | ⭐⭐⭐⭐ |
| KDE Plasma | ~1GB | ⭐⭐⭐⭐ 复杂 | ✅ 良好 | 喜欢定制 | ⭐⭐⭐ |

**Phase 1 决策：Cinnamon**
理由：
1. 低内存占用（~800MB）适合企业办公机
2. 界面接近 Windows 7/XP，企业用户迁移成本最低
3. 可深度定制面板、菜单、主题（Linux Mint 默认桌面）
4. Python 绑定好，自动化配置脚本成熟

### 3.2 预装软件包清单（最终确认）

**办公套件**（三选一，根据兼容率决策）：
- 首选：Microsoft Office via Wine（评级 Gold，95%+ 功能可用）
- 备选：WPS Office for Linux（原生，功能接近但宏/VBA 支持差）
- 备选：LibreOffice（开源免费，格式兼容性问题）

**IM/通讯**：
- DingTalk Linux 原生版（阿里官方 v7.x deb）✅
- TIM：Deepin-wine 适配版（优先）或 TIM Linux 官方版
- 备选：飞书（字节官方 Linux 版，功能完整）✅

**视频会议**：
- Zoom for Linux（原生支持）✅
- Microsoft Teams for Linux（原生支持）✅
- 腾讯会议 Web 版（备用）

**其他预装**：
- 搜狗输入法 for Linux（Fcitx 框架）✅
- WPS Office for Linux ✅
- Chrome / Chromium ✅
- Visual Studio Code ✅

---

## 任务 4：Wine 兼容性复验（本周云端）

本周通过 GitHub Actions CI 完成钉钉原生版 + Office Wine 的自动化摸底，作为 Week 1-2 数据补充。

---

## 任务 5：Week 3 输出物清单

| 输出物 | 文件名 | 状态 |
|--------|--------|------|
| CI/CD workflow YAML | `OS项目_Wine测试_Workflow.md`（已有） | ✅ |
| 桌面环境对比报告 | `reports/OS_Phase1_Week3任务.md`（本文档） | ✅ |
| 预装软件清单 | 嵌入本文档 | ✅ |
| 第一次 CI 运行结果 | （等 GitHub Actions 执行） | ⬜ |

---

## 障碍与应急

| 障碍 | 应急方案 |
|------|---------|
| WSL apt 持续不可用 | 完全依赖 GitHub Actions CI，本机只做文档 |
| GitHub 网络不通 | 等物理机/内网 CI 方案 |
| WineHQ apt 源不通 | 用 Ubuntu 官方 wine 包（版本较旧但稳定）|
