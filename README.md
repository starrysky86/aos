# AOS — All in One System

**产品定位**：面向中国市场的 Windows 兼容桌面操作系统，基于 Ubuntu 24.04 LTS，内置 Wine 兼容层和预认证 Windows 应用商店。

## 核心技术栈

| 层级 | 技术选型 | 版本 |
|------|---------|------|
| Base OS | Ubuntu | 24.04 LTS |
| Desktop | Cinnamon | 6.0.4 |
| Wine | Wine (Ubuntu) | 9.0 |
| IME | Fcitx5 + Rime (雾凇) | 5.1.7 / 5.1.4 |
| Init | systemd | 默认 |
| Package | APT (deb) | — |

## 许可证

所有核心组件采用 OSI 认证开源许可证（GPL/LGPL/BSD/MIT），**零商业纠纷风险**。  
详见 [LICENSE_COMPLIANCE.md](LICENSE_COMPLIANCE.md)。

## 里程碑

| 阶段 | 内容 | 状态 |
|------|------|------|
| Phase 1 | 桌面 OS 构建（12 周） | 🔄 Week 3 进行中 |
| Phase 2 | Wine 认证商店 | 📋 规划中 |
| Phase 3 | 原生扩展 | 📋 规划中 |

## 构建

```bash
# 安装依赖（Ubuntu 24.04）
apt install cinnamon wine fcitx5 fcitx5-rime debootstrap squashfs-tools xorriso

# 构建 ISO
bash scripts/build-iso.sh
```

## 文档结构

```
reports/         # 阶段报告和技术文档
packages/        # 预装软件包
.github/        # CI/CD workflows
scripts/         # 构建脚本
docs/            # 技术架构文档
```
