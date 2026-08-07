# 言面 Flutter 架构方案

**编写人：** 小林（技术架构视角）
**项目：** 言面 = 好来好往（AI 话术工具 APP）
**基于：** 小安《好来好往_市场调研与产品规划报告》
**日期：** 2026-08-06
**状态：** v1.0，可执行

---

## 一、项目概述与产品定位

### 1.1 产品定义

| 字段 | 内容 |
|------|------|
| **产品名称** | 言面（好来好往） |
| **一句话描述** | AI 话术助手，用户输入情境/语音，< 1 秒输出多版本话术建议 |
| **核心交互** | 场景选择 → 语音/文字输入 → AI 输出 → 一键复制 |
| **目标平台** | iOS + Android 双端（Flutter 跨平台） |
| **技术栈核心** | Flutter + Dart + AI 模型 + ASR 语音识别 |

### 1.2 核心功能清单

| 功能 | 优先级 | 说明 |
|------|--------|------|
| 场景选择（情侣/职场/社交/亲子/通用） | P0 | 场景标签是产品核心差异化 |
| 文字输入 → 话术建议 | P0 | 输入框 + 发送按钮 |
| 语音输入 → 实时转写 → 话术建议 | P0 | ASR 实时识别 + 话术生成联动 |
| 多版本话术输出（情商/真诚/轻松版） | P0 | 3 个并行建议卡片 |
| 一键复制到剪贴板 | P0 | 点击即复制，toast 提示 |
| 话术收藏/历史记录 | P1 | 本地 SQLite |
| 会员体系（免费限额/会员无限） | P1 | 次数限制 + 订阅计费 |
| 用户画像/使用数据看板 | P2 | 留存分析 |

### 1.3 非功能需求

- **响应速度**：从输入完成到话术展示 < 1 秒（用户体验核心指标）
- **离线能力**：基础文字话术可本地缓存，AI 生成依赖网络
- **隐私**：对话内容不持久化到云端（会员话术库除外，需用户主动开启）
- **兼容性**：iOS 13+ / Android 8.0+

---

## 二、技术架构总览

### 2.1 架构分层

```
┌─────────────────────────────────────────┐
│              UI 层（Presentation）         │
│   Screens / Widgets / Controllers        │
├─────────────────────────────────────────┤
│            业务逻辑层（Domain）           │
│   Use Cases / Entities / Repositories   │
├─────────────────────────────────────────┤
│              数据层（Data）               │
│   Repository Impl / Data Sources / DTOs │
├─────────────────────────────────────────┤
│             基础设施层（Infra）           │
│   网络 / 存储 / ASR / AI API / 统计      │
└─────────────────────────────────────────┘
```

### 2.2 核心模块依赖关系

```
平台层（iOS/Android）
    ↑
Flutter Framework（Platform Channel）
    ↑
Infra: 网络库（Dio）│ 存储（SQLite/Hive）│ ASR SDK │ AI SDK
    ↑
Data: Repository 实现层
    ↑
Domain: Use Case（生成话术 / 语音转文字 / 收藏话术 / 会员验证）
    ↑
Presentation: BLoC/Provider 状态管理
    ↑
UI: Screen 页面 + Widget 组件
```

### 2.3 项目目录结构

```
lib/
├── main.dart
├── app.dart
│
├── core/                          # 核心基础设施（全局）
│   ├── config/                    # 环境配置（API 地址/密钥/开关）
│   │   ├── app_config.dart
│   │   └── env_dev.dart / env_prod.dart
│   ├── network/                   # HTTP 客户端封装
│   │   ├── dio_client.dart
│   │   └── api_interceptors.dart
│   ├── storage/                   # 本地持久化
│   │   ├── hive_service.dart      # 轻量 KV 存储（设置/Token）
│   │   └── sqlite_service.dart    # 话术历史记录
│   ├── constants/                 # 常量（场景标签/文案/颜色）
│   │   └── app_constants.dart
│   └── utils/                     # 工具函数
│       ├── clipboard_util.dart
│       └── keyboard_util.dart
│
├── features/                      # 按功能模块划分
│   │
│   ├── home/                      # 首页场景选择
│   │   ├── presentation/
│   │   │   ├── home_screen.dart
│   │   │   └── widgets/
│   │   │       ├── scene_card.dart
│   │   │       └── quick_scene_bar.dart
│   │   ├── domain/
│   │   │   └── entities/
│   │   │       └── scene.dart
│   │   └── data/
│   │
│   ├── chat/                      # 话术聊天（核心场景）
│   │   ├── presentation/
│   │   │   ├── chat_screen.dart
│   │   │   ├── bloc/
│   │   │   │   ├── chat_bloc.dart
│   │   │   │   ├── chat_event.dart
│   │   │   │   └── chat_state.dart
│   │   │   └── widgets/
│   │   │       ├── input_bar.dart       # 文字输入
│   │   │       ├── voice_input.dart     # 语音输入 UI
│   │   │       ├── suggestion_card.dart # 话术建议卡片
│   │   │       └── copy_button.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── user_message.dart
│   │   │   │   └── suggestion_reply.dart
│   │   │   └── usecases/
│   │   │       ├── generate_suggestions.dart
│   │   │       └── speech_to_text.dart
│   │   └── data/
│   │       ├── repositories/
│   │       │   └── chat_repository_impl.dart
│   │       ├── datasources/
│   │       │   ├── ai_remote_datasource.dart  # AI API 调用
│   │       │   └── asr_remote_datasource.dart # 语音识别 API
│   │       └── models/
│   │           └── suggestion_model.dart
│   │
│   ├── history/                   # 话术历史记录
│   │   ├── presentation/
│   │   │   ├── history_screen.dart
│   │   │   └── bloc/
│   │   ├── domain/
│   │   │   └── entities/
│   │   │       └── history_item.dart
│   │   └── data/
│   │       ├── repositories/
│   │       └── datasources/
│   │           └── history_local_datasource.dart
│   │
│   ├── member/                    # 会员中心
│   │   ├── presentation/
│   │   │   ├── member_screen.dart
│   │   │   └── bloc/
│   │   └── data/
│   │       └── datasources/
│   │           └── member_remote_datasource.dart
│   │
│   └── settings/                  # 设置
│       └── presentation/
│           └── settings_screen.dart
│
└── shared/                         # 跨功能共享
    ├── widgets/
    │   ├── loading_overlay.dart
    │   ├── error_toast.dart
    │   └── copy_to_clipboard.dart
    └── theme/
        ├── app_theme.dart
        └── app_colors.dart
```

---

## 三、核心模块详细设计

### 3.1 AI 话术生成模块（最关键）

**Use Case 类**：`GenerateSuggestionsUseCase`

```dart
// 输入
class GenerateSuggestionsParams {
  final String scenario;       // '情侣' | '职场' | '社交' | '亲子' | '通用'
  final String userInput;      // 用户原始输入
  final String tone;           // '情商' | '真诚' | '轻松'
}

// 输出
class SuggestionReply {
  final String text;           // 话术内容
  final String tone;           // 所属语气
  final bool isPremium;        // 是否需要会员
  final DateTime generatedAt;
}
```

**调用链路**：
```
用户输入 → ChatBloc.add(SubmitMessageEvent) 
  → GenerateSuggestionsUseCase 
    → AI API (通义千问/智谱GLM) 
      → 解析 JSON 返回 
        → 3 个 SuggestionReply 
          → ChatBloc.emit(SuggestionsLoaded)
            → UI 渲染 3 张卡片
```

**Prompt 模板设计**（关键差异化）：

```
系统：你是一个专业的话术助手，帮助用户在特定场景下给出得体、真诚、温暖的回答。
用户情境：{scenario}
用户原话：{userInput}

请给出 3 个版本的回复建议，JSON 格式：
{
  "情商版": "...",
  "真诚版": "...",
  "轻松版": "..."
}

要求：
- 每条不超过 50 字
- 贴合 {scenario} 场景
- 情商版：高情商但不套路
- 真诚版：直接真诚，不绕弯子
- 轻松版：轻松幽默，缓解气氛
- 不要假大空，要真实可用的回复
```

**API 集成**：首选用通义千问（成本低 + 国内合规），备选智谱 GLM-4。

### 3.2 语音输入模块

**架构**：ASR 实时转文字，通过 Platform Channel 接入原生 SDK。

| 方案 | 推荐度 | 说明 |
|------|--------|------|
| **阿里 ASR（智能 voice）** | ⭐⭐⭐⭐ | 实时转写效果好，有 Flutter SDK，支持流式 |
| 腾讯 ASR | ⭐⭐⭐ | 同上，二选一 |
| 讯飞 ASR | ⭐⭐ | 老牌，但 SDK 集成复杂 |
| Web Speech API | ⭐⭐ | 仅 Web，iOS Safari 支持差 |

**交互设计**：
- 按住说话按钮（iOS/Android 原生风格）
- 实时显示转写文字（流式输出）
- 松开自动触发话术生成（减少一步操作）

```dart
// 语音输入 Bloc 事件流
VoiceButtonPressed → VoiceListening
  → ASR Streaming Result → VoiceTextUpdated
    → VoiceButtonReleased → SubmitTextEvent
      → GenerateSuggestions (复用文字输入逻辑)
```

### 3.3 状态管理方案

**选择：BLoC 模式**（推荐理由：团队协作清晰、便于单元测试、状态可追溯）

| 页面/功能 | BLoC | 状态 |
|---------|------|------|
| 首页场景 | `SceneBloc` | `SceneInitial / SceneLoaded` |
| 话术生成 | `ChatBloc` | `ChatIdle / ChatLoading / ChatLoaded / ChatError` |
| 语音输入 | `VoiceBloc` | `VoiceIdle / VoiceListening / VoiceProcessing` |
| 历史记录 | `HistoryBloc` | `HistoryLoaded(items) / HistoryEmpty` |
| 会员状态 | `MemberBloc` | `MemberFree(remaining) / MemberPremium` |

### 3.4 本地存储设计

**Hive（轻量 KV）**：存放 Token、用户设置、会员状态

```dart
// Hive Box 结构
box_user: { token, userId, isPremium, premiumExpireAt }
box_settings: { theme, defaultScenario, asrLanguage }
box_cache: { lastUsedScenarios, cachedPrompts }
```

**SQLite（话术历史）**：存放用户生成过的话术记录

```sql
CREATE TABLE history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scenario TEXT NOT NULL,
  user_input TEXT NOT NULL,
  suggestion_text TEXT NOT NULL,
  tone TEXT NOT NULL,          -- '情商' / '真诚' / '轻松'
  is_favorited INTEGER DEFAULT 0,
  created_at TEXT NOT NULL
);
```

---

## 四、API 接口设计

### 4.1 后端 API（Node.js / Python FastAPI）

| 接口 | Method | 说明 | 请求体 |
|------|--------|------|--------|
| `/api/v1/suggest` | POST | 生成话术建议 | `{ scenario, userInput, userId? }` |
| `/api/v1/asr` | POST | 语音转文字（代理阿里 ASR） | `{ audioBase64 }` |
| `/api/v1/member/status` | GET | 查询会员状态 | Header: `Authorization` |
| `/api/v1/member/verify` | POST | 验证订阅收据（防破解） | `{ receiptData }` |
| `/api/v1/history/sync` | POST | 同步历史（需登录） | `{ items[] }` |

### 4.2 话术生成响应格式

```json
{
  "success": true,
  "data": {
    "suggestions": [
      {
        "tone": "情商版",
        "text": "我理解你的感受，我们找个时间好好聊聊吧。",
        "isPremium": false
      },
      {
        "tone": "真诚版",
        "text": "这件事我确实没处理好，对不起。",
        "isPremium": false
      },
      {
        "tone": "轻松版",
        "text": "哎呀，别生气了，我请你喝奶茶赔罪！",
        "isPremium": true
      }
    ],
    "remainingFreeCount": 7,
    "modelUsed": "qwen-turbo"
  }
}
```

---

## 五、UI/UX 设计方向

### 5.1 页面结构

```
启动页 (SplashScreen)
  ↓ 自动跳转
首页 (HomeScreen)
  ├─ 场景选择卡片（情侣/职场/社交/亲子/通用）
  ├─ 快捷入口（最近使用场景）
  └─ 底部导航栏
       ├─ 首页
       ├─ 历史
       ├─ 会员（中心入口）
       └─ 设置

点击场景 → 话术聊天页 (ChatScreen)
  ├─ 顶部：场景标签 + 切换按钮
  ├─ 中部：话术建议卡片列表（3 张）
  ├─ 底部：输入框 + 语音按钮 + 发送按钮
  └─ 空状态：引导输入

历史页 (HistoryScreen)
  ├─ Tab: 收藏 / 全部
  └─ 列表：时间分组话术记录

会员页 (MemberScreen)
  ├─ 当前状态展示（免费次数 / 到期日）
  ├─ 订阅按钮（¥9.9/月 / ¥69/年）
  └─ 恢复购买按钮
```

### 5.2 设计规范

| 维度 | 规范 |
|------|------|
| 设计风格 | 温暖卡片式，圆角 16px，轻阴影 |
| 主色调 | #FF8A65（珊瑚橙，温暖感） |
| 辅助色 | #4CAF50（确认/成功），#FF5252（会员专属） |
| 字体 | 系统默认（iOS SF / Android Roboto） |
| 动效 | 话术卡片淡入（300ms ease-out），语音波形实时跳动 |
| 隐私 | 录音时显示红色录音指示器 |

---

## 六、技术选型汇总

| 层级 | 技术选型 | 理由 |
|------|---------|------|
| **跨平台框架** | Flutter 3.x | iOS + Android 双端，热点 |
| **状态管理** | flutter_bloc ^8.x | BLoC 模式，测试友好 |
| **HTTP 客户端** | dio ^5.x | 拦截器、自动重试、适配器 |
| **本地 KV 存储** | hive ^2.x | 轻量，比 SharedPreferences 快 |
| **本地数据库** | sqflite ^2.x | 话术历史，SQL 查询强 |
| **AI 模型** | 通义千问（qwen-turbo） | 成本低，国内合规 |
| **ASR 语音识别** | 阿里 ASR（智能 voice） | 实时流式，效果好 |
| **路由管理** | go_router ^14.x | 声明式路由，深度链接支持 |
| **依赖注入** | get_it ^7.x | 服务定位器，简单直接 |
| **构建/发布** | Codemagic / GitHub Actions | Flutter CI/CD |

---

## 七、Phase 1 开发计划（4–6 周 MVP）

### Week 1–2：项目骨架 + 首页

- [ ] Flutter 项目初始化（Clean Architecture 目录结构）
- [ ] 路由配置（go_router）
- [ ] 状态管理框架搭建（flutter_bloc）
- [ ] 首页 UI + 场景选择逻辑
- [ ] 底部导航栏

### Week 3：话术生成核心

- [ ] AI API 集成（通义千问）
- [ ] 话术生成 BLoC 逻辑
- [ ] 话术卡片 UI（3 张并行展示）
- [ ] 复制到剪贴板功能
- [ ] 加载/错误状态处理

### Week 4：语音输入

- [ ] 阿里 ASR Flutter 插件集成
- [ ] 语音输入 BLoC
- [ ] 按住说话 UI + 实时转写展示
- [ ] 语音松开自动触发话术生成

### Week 5：历史 + 本地存储

- [ ] Hive 初始化（Token、设置）
- [ ] SQLite 话术历史存储
- [ ] 历史页面 UI
- [ ] 收藏/取消收藏功能

### Week 6：会员 + 收尾

- [ ] 会员 API 集成
- [ ] 免费次数限制逻辑
- [ ] 会员页 UI
- [ ] iOS/Android 打包测试
- [ ] MVP 内部测试 + 修复

**MVP 验收标准**：
- 输入任意场景 + 文字 → < 1.5 秒显示 3 个版本话术
- 语音输入 → 实时转写 → 话术生成全链路跑通
- 话术历史记录保存和展示
- iOS + Android 双端均可打包安装

---

## 八、技术风险与应对

| 风险 | 概率 | 影响 | 应对预案 |
|------|------|------|---------|
| AI API 响应慢（> 2 秒） | 高 | 用户体验差 | 前端加骨架屏 + 本地缓存高频场景话术模板兜底 |
| 阿里 ASR 识别准确率低 | 中 | 语音输入不可用 | 识别失败时自动回退到文字输入，并提示"未识别成功" |
| App Store 审核拒绝（ASR 权限） | 低 | 发版延误 | 申请权限时明确隐私政策说明，仅后台录音 |
| 模型费用超预算 | 中 | 运营成本高 | 早期接入免费额度（通义千问有赠送），中期按需付费 |
| iOS/Android 行为不一致 | 中 | QA 工作量 | 每周双端真机联调，不依赖模拟器 |

---

## 九、后续扩展方向（Phase 2/3）

| 方向 | 说明 |
|------|------|
| **话术场景扩展** | 销售话术/投诉处理/面试等垂直场景包 |
| **AI 模型 Fine-tune** | 收集用户反馈数据，微调专属话术模型 |
| **微信小程序版** | 降低使用门槛，无需下载 |
| **企业版（B 端）** | 销售话术 CRM 集成 + 团队管理 |
| **社区 UGC** | 用户贡献优质话术，评分排行 |

---

*本方案基于小安《好来好往_市场调研与产品规划报告》扩展，整合为可直接落地的 Flutter 架构。*
*如需进一步细化 API 文档、数据库 Schema 或 UI 设计稿，随时告知。*
