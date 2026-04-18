# 第三批游戏验收报告

> 验收日期：2026-04-18  
> 验收范围：第三批 6 个游戏 + 首页新卡片

---

## 整体结论：✅ 全部通过，无 Backlog

---

## 结构检查

| 检查项 | 结果 |
|--------|------|
| 6 个游戏目录均存在 | ✅ |
| 所有路径均用 `../../shared.css` / `../../game-utils.js` | ✅ |
| 5 关游戏：intro + 5 关 + complete = 7 屏（mysql_index / redis_ha / tcp_handshake）| ✅ |
| 4 关游戏：intro + 4 关 + complete = 6 屏（dist_lock / mysql_recovery / mongodb_selector）| ✅ |
| G_TOTAL 与关卡数一致（5关=5 / 4关=4）| ✅ |
| `completeLevel` 全部从反馈区「继续」按钮触发，不直接跳关 | ✅ |
| 首页 6 张新卡片全部链接（去掉「即将推出」状态）| ✅ |

---

## 逐游戏验收

### ⑧ SQL 查询路径追踪器 `mysql/mysql_index/` · 499 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#7c83ff`（紫）| ✅ |
| intro + 5 关 + complete | ✅ |
| B+ 树 SVG 渲染，节点可点击（`clickBNode`），走查询路径后节点变色（active / visited / found）| ✅ |
| L2：主键查询 vs 回表判断 | ✅ |
| 覆盖索引、联合索引考点覆盖 | ✅ |

---

### ⑨ Redis 高可用演练 `redis/redis_ha/` · 507 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#ef4444`（红）| ✅ |
| intro + 5 关 + complete | ✅ |
| 拓扑图：1 主 2 从 + 3 哨兵节点可视化（master / slave / sentinel 样式分色）| ✅ |
| L2：哨兵步骤序列按钮（step-btns）— 发现故障 → 发起投票 → 选主 → 故障转移 | ✅ |
| 主从复制、投票、Sentinel failover 全流程覆盖 | ✅ |

---

### ⑩ TCP 握手挥手模拟器 `network/tcp_handshake/` · 503 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#3b82f6`（蓝）| ✅ |
| intro + 5 关 + complete | ✅ |
| 玩家扮演客户端，点击 SYN / ACK / FIN / SYN-ACK / RST 报文按钮主动发包 | ✅ |
| 报文动画（c2s 蓝色 / s2c 绿色 / both 紫色）视觉区分 | ✅ |
| 三次握手 + 四次挥手 + 异常场景全覆盖 | ✅ |

---

### ⑪ 分布式锁方案裁判 `distributed/dist_lock/` · 347 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#10b981`（绿）| ✅ |
| intro + 4 关 + complete | ✅ |
| L1：SETNX / Redlock / ZooKeeper 对比表 + 选型判断 | ✅ |
| L2：Redis 主节点宕机场景 — SETNX 锁是否安全 | ✅ |
| 主节点宕机数据安全性分析覆盖 | ✅ |

---

### ⑫ MySQL 崩溃恢复 `mysql/mysql_recovery/` · 407 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#f59e0b`（橙）| ✅ |
| intro + 4 关 + complete | ✅ |
| WAL 时间轴（wal-timeline）可视化，标注 redo log / binlog 写入顺序 | ✅ |
| L2：两阶段提交流程 + 崩溃点判断（crash-marker）| ✅ |
| WAL · redo log · binlog · 两阶段提交全考点覆盖 | ✅ |

---

### ⑬ MongoDB 场景选型 `distributed/mongodb_selector/` · 404 行

| 检查项 | 结果 |
|--------|------|
| 主题色 `#10b981`（绿）| ✅ |
| intro + 4 关 + complete | ✅ |
| Schema 对比展示（MongoDB 文档结构 vs MySQL 表结构）| ✅ |
| 给业务需求选 MongoDB vs MySQL + 理由，vs-card 双列布局 | ✅ |

---

## Backlog

无。第三批全部符合规划要求。

---

## 项目完结总结

全部 13 个游戏开发完毕：

| 批次 | 游戏数 | 状态 |
|------|--------|------|
| 迁移 | 2（MVCC / IO多路复用）| ✅ 完成 |
| 第一批 | 4（GC三色 / 并发审判 / 协程侦探 / Redis诊断）| ✅ 完成，2处交互已补强 |
| 第二批 | 3（GMP调度 / MySQL锁 / 流量风暴）| ✅ 完成，L3交互已补强 |
| 第三批 | 6（索引追踪 / Redis HA / TCP握手 / 分布式锁 / 崩溃恢复 / MongoDB选型）| ✅ 完成 |
| **合计** | **13 个游戏** | **✅ 全部上线** |
