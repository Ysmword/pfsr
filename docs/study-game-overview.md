# 学习游戏中心 · 项目总体介绍

> 本文档面向新同学入门，以及每次与 AI 协作开发时的上下文速查。
> 读完本文，可独立理解项目结构、开发规范，并能上手新游戏的开发。

---

## 一、项目定位

`study_game/` 是一套**纯前端的交互式学习游戏集合**，服务于后端工程师面试备考。

核心理念：**亲手操作 > 阅读选择 > 死记硬背**。每个游戏 4-12 分钟，覆盖一个高频面试考点，通过拖拽、点击、参数调节等交互，让知识从"读过"变成"做过"。

技术栈：**纯 HTML + CSS + 原生 JavaScript，零依赖，无构建工具**。所有文件可直接在浏览器打开。

---

## 二、目录结构

```
study_game/
├── shared.css              ← 全局设计系统（不要随意修改）
├── game-utils.js           ← 两个核心工具函数（不要随意修改）
├── _template/              ← 新游戏起始模板（cp 后改内容）
│   └── index.html
├── index.html              ← 游戏中心首页
│
├── go/                     ← Go 运行时 & 并发（4 个游戏）
│   ├── gc_simulator/       ✅ GC 三色标记模拟器
│   ├── concurrency_court/  ✅ 并发 Bug 代码审判
│   ├── goroutine_detective/✅ 协程泄漏侦探
│   └── gmp_scheduler/      ✅ GMP 调度模拟器
│
├── redis/                  ← Redis（2 个游戏）
│   ├── redis_diagnosis/    ✅ Redis 故障诊断室
│   └── redis_ha/           ✅ Redis 高可用演练
│
├── mysql/                  ← MySQL（4 个游戏）
│   ├── mvcc/               ✅ MVCC 闯关游戏
│   ├── mysql_lock/         ✅ MySQL 锁冲突判断
│   ├── mysql_index/        ✅ SQL 查询路径追踪器
│   └── mysql_recovery/     ✅ MySQL 崩溃恢复
│
├── network/                ← 计算机网络（2 个游戏）
│   ├── io_multiplexing/    ✅ I/O 多路复用模拟器
│   └── tcp_handshake/      ✅ TCP 握手挥手模拟器
│
├── distributed/            ← 分布式 & 系统设计（3 个游戏）
│   ├── rate_limiter/       ✅ 流量风暴生存
│   ├── dist_lock/          ✅ 分布式锁方案裁判
│   └── mongodb_selector/   ✅ MongoDB 场景选型
│
└── confidence/             ← 其他（1 个）
    └── ...                 ✅ 我本如此（自信构建）
```

> **注意**：根目录下的 `mvcc/`、`io_multiplexing/` 是历史遗留目录，正式版已迁移至上方分类目录，请以分类目录为准。

---

## 三、设计系统（shared.css）

所有游戏共享同一套设计令牌，深色主题，主色可被每个游戏覆盖。

### 颜色令牌

| 变量 | 值 | 用途 |
|------|----|------|
| `--bg` | `#0f0f1a` | 页面背景 |
| `--surface` | `#1a1a2e` | 卡片/面板背景 |
| `--border` | `#2a2a4a` | 边框 |
| `--text` | `#e0e0e0` | 主文字 |
| `--text-muted` | `#8888a8` | 次要文字 |
| `--text-dim` | `#55556a` | 辅助文字/标签 |
| `--success` | `#10b981` | 成功/正确 |
| `--warning` | `#f59e0b` | 警告 |
| `--danger` | `#ef4444` | 错误/危险 |
| `--accent` | 每游戏覆盖 | 主题色（按钮、标题、高亮） |
| `--accent-dim` | 每游戏覆盖 | 主题色半透明，用于阴影/发光 |

### 各分类主题色

| 分类 | 主题色 | 变量值 |
|------|--------|--------|
| Go 运行时 & 并发 | 青色 | `#00d4ff` |
| Redis | 红色 | `#ef4444` |
| MySQL | 紫色 | `#7c83ff` |
| 计算机网络 | 蓝色 | `#3b82f6` |
| 分布式 & 系统设计 | 绿色 | `#10b981` |

### 核心 UI 组件

shared.css 已内置以下组件，**游戏内直接使用 class，无需重写样式**：

- `.game-topbar` — 顶部导航栏（返回按钮 + 标题 + 进度点）
- `.screen` / `.screen.active` — 屏幕切换容器（同一时间只显示一个 active 的 screen）
- `.btn` + `.btn-primary` / `.btn-success` / `.btn-ghost` 等 — 按钮组
- `.card` / `.card--accent` — 内容卡片
- `.game-intro` — 游戏介绍首屏组件
- `.level-complete` — 关卡完成提示卡片
- `.complete-screen` — 通关庆祝屏（带扩散光环动画）
- `.fade-in` / `.fade-in-slow` — 淡入动画工具类
- `.text-accent` / `.text-success` 等 — 文字颜色工具类

---

## 四、工具函数（game-utils.js）

仅提供两个核心功能：

### `TopbarProgress`

管理顶部进度点的状态。

```javascript
// 更新进度：第 n 关激活，前 n-1 关标记已完成
TopbarProgress.update({ activeIndex: 2, doneUpTo: 2 });

// 全部完成（通关时调用）
TopbarProgress.completeAll();

// 重置（重玩时调用）
TopbarProgress.reset();
```

### `showScreen(id)`

切换显示的屏幕，自动滚动到顶部。

```javascript
showScreen('intro');      // 显示 #screen-intro
showScreen('level-1');    // 显示 #screen-level-1
showScreen('complete');   // 显示 #screen-complete
```

---

## 五、游戏 HTML 结构规范

每个游戏是一个**单 HTML 文件**，结构固定分为 8 个部分：

```
① <head> 引入 shared.css（子目录用 ../../shared.css）
② <style> 覆盖主题色 + 游戏专属样式
③ <nav class="game-topbar"> 顶部导航（改标题 + dot 数量）
④ #screen-intro 游戏介绍屏
⑤ #screen-level-N 各关卡屏（N 从 1 开始）
⑥ #screen-complete 通关屏
⑦ <script src="../../game-utils.js"> 引入工具
⑧ <script> 游戏逻辑
```

### 路径规则

| 文件位置 | shared.css 路径 | game-utils.js 路径 |
|---------|----------------|-------------------|
| `study_game/index.html` | `shared.css` | — |
| `study_game/{game}/index.html` (一级) | `../shared.css` | `../game-utils.js` |
| `study_game/{cat}/{game}/index.html` (二级，当前标准) | `../../shared.css` | `../../game-utils.js` |
| 后退按钮 `href` | 统一用绝对路径 `/study_game/`，无需关心层级 |

---

## 六、关卡交互规范

### 反馈卡片（每关必须有）

每关提交答案后，必须显示标准反馈卡片，包含：
- **裁判词**：一句话解释真正原因（错误时的解释比正确时更重要）
- **继续按钮**：玩家点击后才调用 `completeLevel(n)` 跳下一关

```html
<div class="feedback-card" id="level1Feedback">
  <div class="feedback-card__verdict" id="level1Verdict"></div>
  <p class="feedback-card__explain" id="level1Explain"></p>
  <div style="text-align:center;">
    <button class="btn btn-primary" onclick="completeLevel(1)">继续 →</button>
  </div>
</div>
```

```javascript
// 提交时根据对错设置样式和文字
const fb = document.getElementById('level1Feedback');
fb.className = 'feedback-card ' + (correct ? 'correct' : 'wrong');
document.getElementById('level1Verdict').textContent = correct ? '✓ 正确！' : '✗ 答错了';
document.getElementById('level1Explain').textContent = '解释文字...';
fb.style.display = 'block';
```

### 标准关卡流程函数

```javascript
const G = { totalLevels: 5 };

function startGame() {
  showScreen('level-1');
  TopbarProgress.update({ activeIndex: 0 });
}

function completeLevel(n) {
  const next = n + 1;
  TopbarProgress.update({ doneUpTo: n, activeIndex: next <= G.totalLevels ? next - 1 : -1 });
  if (n < G.totalLevels) {
    showScreen('level-' + next);
  } else {
    TopbarProgress.completeAll();
    showScreen('complete');
  }
}

function resetGame() {
  TopbarProgress.reset();
  // 重置游戏专属状态...
  showScreen('intro');
}
```

---

## 七、已完成游戏清单

### Go 运行时 & 并发

| 游戏 | 路径 | 关卡数 | 时长 | 核心考点 |
|------|------|--------|------|---------|
| GC 三色标记模拟器 | `go/gc_simulator/` | 5 关 | 10min | 三色标记、混合写屏障、GC 演进 |
| 并发 Bug 代码审判 | `go/concurrency_court/` | 6 关 | 12min | Mutex、RWMutex、WaitGroup、Channel、defer、select |
| 协程泄漏侦探 | `go/goroutine_detective/` | 5 关 | 10min | context 取消传播、goroutine 生命周期 |
| GMP 调度模拟器 | `go/gmp_scheduler/` | 5 关 | 10min | G/M/P 三角关系、Work Stealing、Hand Off、G0/M0 |

### Redis

| 游戏 | 路径 | 关卡数 | 时长 | 核心考点 |
|------|------|--------|------|---------|
| Redis 故障诊断室 | `redis/redis_diagnosis/` | 5 关 | 10min | 热key、大key、缓存穿透/击穿/雪崩、slowlog |
| Redis 高可用演练 | `redis/redis_ha/` | 5 关 | 10min | 哨兵机制、主从复制、故障转移投票 |

### MySQL

| 游戏 | 路径 | 关卡数 | 时长 | 核心考点 |
|------|------|--------|------|---------|
| MVCC 闯关游戏 | `mysql/mvcc/` | 6 关 | 15min | 版本链、ReadView、RC/RR 可见性 |
| MySQL 锁冲突判断 | `mysql/mysql_lock/` | 5 关 | 12min | 间隙锁、临键锁、死锁检测 |
| SQL 查询路径追踪器 | `mysql/mysql_index/` | 5 关 | 10min | B+ 树、回表、覆盖索引、最左前缀 |
| MySQL 崩溃恢复 | `mysql/mysql_recovery/` | 4 关 | 8min | WAL、redo log、binlog 两阶段提交 |

### 计算机网络

| 游戏 | 路径 | 关卡数 | 时长 | 核心考点 |
|------|------|--------|------|---------|
| I/O 多路复用模拟器 | `network/io_multiplexing/` | 9 关 | 12min | select → poll → epoll 演进 |
| TCP 握手挥手模拟器 | `network/tcp_handshake/` | 5 关 | 10min | 三次握手、四次挥手、TIME_WAIT |

### 分布式 & 系统设计

| 游戏 | 路径 | 关卡数 | 时长 | 核心考点 |
|------|------|--------|------|---------|
| 流量风暴生存 | `distributed/rate_limiter/` | 5 关 | 10min | 限流算法、令牌桶、熔断三态 |
| 分布式锁方案裁判 | `distributed/dist_lock/` | 4 关 | 8min | SETNX、Redlock、ZooKeeper 临时节点 |
| MongoDB 场景选型 | `distributed/mongodb_selector/` | 4 关 | 8min | 文档模型 vs 关系模型适用边界 |

---

## 八、新增游戏 SOP

开发一个新游戏的完整步骤：

```bash
# 1. 从模板复制到目标路径
cp -r study_game/_template study_game/{category}/{game_name}/
```

**必改项（`index.html`）：**

1. `<title>` — 改为「游戏名 - 学习游戏中心」
2. `:root` — 覆盖 `--accent` 和 `--accent-dim`（参考分类主题色）
3. 路径 — `../shared.css` 改为 `../../shared.css`；`../game-utils.js` 改为 `../../game-utils.js`
4. `.game-topbar__title` — 改为游戏名称
5. `.game-topbar__dot` — 按关卡数量增删 dot 元素
6. `#screen-intro` — 改图标、标题、描述、时长、关卡数
7. 关卡屏 — 按关卡数量复制 `#screen-level-N` 模板，填充交互内容
8. `#screen-complete` — 改通关总结语
9. `G.totalLevels` — 与实际关卡数保持一致

**在首页注册（`study_game/index.html`）：**

在对应分类的 `.cards` 里加一个 `.game-card`：

```html
<a class="game-card cat-{分类}" href="/study_game/{category}/{game_name}/">
  <div class="card-icon">🎯</div>
  <div class="card-name">游戏名称</div>
  <div class="card-desc">一句话描述核心体验。</div>
  <div class="card-meta">
    <span class="card-tag">标签1</span>
    <span class="card-tag">标签2</span>
    <span class="card-time">N关 · Nmin</span>
  </div>
</a>
```

---

## 九、关卡设计原则

开发时严格遵守以下原则，保证游戏质量：

1. **亲手操作 > 阅读选择**：能拖拽/点击/填写的，不做单纯单选题
2. **诊断在前，方案在后**：先让玩家判断是什么问题，再选解决方案
3. **每关一个核心概念**：宁可关卡多，不要一关塞三个知识点
4. **错误反馈要有教学价值**：答错后显示的解释比答对更重要
5. **关卡递进**：同一游戏内从「识别概念」→「综合判断」，难度线性上升
6. **反馈卡片必须标准化**：每关提交后必须显示反馈区（正确/错误不同样式），包含一句「裁判词」；`completeLevel()` 只在玩家点击反馈区内的「继续」后才调用，不得直接跳关

---

## 十、相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 完整开发规划 | `docs/study-game-roadmap.md` | 所有游戏的详细关卡设计，含交互形式、核心考点 |
| 第一批评审 | `docs/study-game-batch1-review.md` | Batch 1 验收记录，可参考游戏质量基线 |
| 本文档 | `docs/study-game-overview.md` | 项目总体介绍（当前文件） |
