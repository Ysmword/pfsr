# 学习游戏中心 · 失败机制设计方案

> 解决问题：答错关卡后仍显示通关屏，体验不符合实际。
> 本文档同时作为实现规范，供后续 AI 协作时快速上下文同步。

---

## 一、问题描述

所有游戏的关卡流程：

```
[提交答案] → showFeedback(正确/错误都显示) → [继续按钮] → completeLevel(n) → showScreen('complete')
```

`completeLevel` 完全不感知对错，答对答错都进入通关屏。

---

## 二、设计原则

1. **答错可以继续**：不中途截断学习，玩家可以看完全部关卡内容。
2. **最后统一判定**：所有关卡结束后，根据累计错误数决定进入通关屏还是失败屏。
3. **有 1 关错即失败**：失败屏显示错误关卡数，引导重新挑战。
4. `confidence/` 游戏（自信构建，无对错判断）**不参与此机制**。

---

## 三、改动层次

### 层 1：`game-utils.js`（共享工具，加 Mistakes 单例）

```javascript
const Mistakes = {
  count: 0,
  add()   { this.count++; },
  reset() { this.count = 0; },
  get()   { return this.count; }
};
```

所有游戏通过 `Mistakes.add()` / `Mistakes.reset()` / `Mistakes.get()` 操作，无需各自维护计数器。

---

### 层 2：`shared.css`（加 `.failed-screen` 组件）

结构与 `.complete-screen` 完全对称，颜色替换为 `--danger`（红色）。

```
.failed-screen
  └── .failed-screen__rings        ← 红色扩散光环（同 complete-screen）
  └── .failed-screen__content
        ├── .failed-screen__icon   ← 大图标（💥）
        ├── .failed-screen__title  ← "挑战失败"
        ├── .failed-screen__desc   ← 动态文字，显示错误关数
        └── .failed-screen__actions
              ├── [重新挑战] btn-danger
              └── [返回游戏中心] btn-ghost
```

---

### 层 3：每个游戏 HTML（3 处改动）

#### 改动 ① — 在 `#screen-complete` 后加 `#screen-failed` HTML 块

```html
<!-- ⑦-B 失败屏 -->
<div class="screen" id="screen-failed">
  <div class="failed-screen">
    <div class="failed-screen__rings">
      <div class="failed-screen__ring"></div>
      <div class="failed-screen__ring"></div>
      <div class="failed-screen__ring"></div>
      <div class="failed-screen__ring"></div>
    </div>
    <div class="failed-screen__content fade-in-slow">
      <div class="failed-screen__icon">💥</div>
      <div class="failed-screen__title">挑战失败</div>
      <p class="failed-screen__desc" id="failed-desc"></p>
      <div class="failed-screen__actions">
        <button class="btn btn-danger" onclick="resetGame()">重新挑战</button>
        <a class="btn btn-ghost" href="/study_game/">返回游戏中心</a>
      </div>
    </div>
  </div>
</div>
```

#### 改动 ② — 跟踪错误（在 showFeedback 或 submit 函数中）

有 `showFeedback(prefix, correct/ok, ...)` 共享函数的游戏，在函数内加 1 行：

```javascript
function showFeedback(prefix, correct, ...) {
  if (!correct) Mistakes.add();   // ← 新增
  // ... 原有逻辑
}
```

无共享 showFeedback 的游戏，在各 submit 函数判断错误的地方加：

```javascript
if (!ok) Mistakes.add();
```

#### 改动 ③ — 路由判断 + 重置

```javascript
// completeLevel 末尾
function completeLevel(n) {
  // ... 原有跳屏逻辑
  if (n >= TOTAL) {
    TopbarProgress.completeAll();
    if (Mistakes.get() > 0) {
      document.getElementById('failed-desc').textContent =
        `本次有 ${Mistakes.get()} 关答错了，知识点还需要加强，再来一次！`;
      showScreen('failed');
    } else {
      showScreen('complete');
    }
  }
}

// resetGame 加 Mistakes.reset()
function resetGame() {
  TopbarProgress.reset();
  Mistakes.reset();   // ← 新增
  showScreen('intro');
}
```

---

## 四、游戏改动清单

| 游戏 | 路径 | showFeedback 类型 | 状态 |
|------|------|-----------------|------|
| GC 三色标记模拟器 | `go/gc_simulator/` | 有共享 `showFeedback(prefix, correct, ...)` | ✅ |
| 并发 Bug 代码审判 | `go/concurrency_court/` | 有共享 `showFeedback(prefix, correct, ...)` | ✅ |
| 协程泄漏侦探 | `go/goroutine_detective/` | 有共享 `showFeedback(prefix, correct, ...)` | ✅ |
| GMP 调度模拟器 | `go/gmp_scheduler/` | 无共享，各 submit 内跟踪 | ✅ |
| Redis 故障诊断室 | `redis/redis_diagnosis/` | 有共享 `showFeedback(prefix, ok, ...)` | ✅ |
| Redis 高可用演练 | `redis/redis_ha/` | 无共享，各 submit 内跟踪 | ✅ |
| MVCC 闯关游戏 | `mysql/mvcc/` | 无共享，各 submit 内跟踪 | ✅ |
| MySQL 锁冲突判断 | `mysql/mysql_lock/` | 无共享，各 submit 内跟踪 | ✅ |
| SQL 查询路径追踪器 | `mysql/mysql_index/` | 无共享，各 submit 内跟踪 | ✅ |
| MySQL 崩溃恢复 | `mysql/mysql_recovery/` | 无共享，各 submit 内跟踪 | ✅ |
| I/O 多路复用模拟器 | `network/io_multiplexing/` | 无共享，各 submit 内跟踪 | ✅ |
| TCP 握手挥手模拟器 | `network/tcp_handshake/` | 无共享，各 submit 内跟踪 | ✅ |
| 流量风暴生存 | `distributed/rate_limiter/` | 无共享，各 submit 内跟踪 | ✅ |
| 分布式锁方案裁判 | `distributed/dist_lock/` | 无共享，各 submit 内跟踪 | ✅ |
| MongoDB 场景选型 | `distributed/mongodb_selector/` | 无共享，各 submit 内跟踪 | ✅ |

> `confidence/` 跳过，无对错判断。

---

## 五、新增到 `_template/index.html` 的标准片段

开发新游戏时，模板已包含 `#screen-failed` 块和标准 JS，直接使用即可。

---

## 六、关键约束

- `Mistakes` 对象挂载在 `game-utils.js` 中，所有游戏共享（游戏切换时 `resetGame` 负责清零）
- `failed-desc` 文字在进入失败屏前动态写入
- 失败屏的"重新挑战"调用 `resetGame()`，与通关屏的"再玩一次"完全一致
- 不允许在中途（非最后一关）触发失败屏
