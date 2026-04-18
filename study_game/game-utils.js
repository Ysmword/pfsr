/* =====================================================
   STUDY GAME — Shared Utilities
   study_game/game-utils.js

   在 <script> 标签前引入：
   <script src="../game-utils.js"></script>
===================================================== */

/* ----- Topbar 进度 API -----
   dots 对应 .game-topbar__dot 元素，按 DOM 顺序排列。

   TopbarProgress.update({ activeIndex, doneUpTo })
     activeIndex : 当前激活的 dot 索引（高亮闪烁）
     doneUpTo    : 前 N 个 dot 标记为已完成

   TopbarProgress.completeAll()  — 全部标绿（通关时用）
   TopbarProgress.reset()        — 清除所有状态（重置时用）
----------------------------------------------------- */
const TopbarProgress = (() => {
  function dots() { return document.querySelectorAll('.game-topbar__dot'); }
  return {
    update({ activeIndex = -1, doneUpTo = 0 } = {}) {
      dots().forEach((dot, i) => {
        dot.classList.remove('game-topbar__dot--done', 'game-topbar__dot--active');
        if (i < doneUpTo)           dot.classList.add('game-topbar__dot--done');
        else if (i === activeIndex) dot.classList.add('game-topbar__dot--active');
      });
    },
    completeAll() {
      dots().forEach(d => {
        d.classList.remove('game-topbar__dot--active');
        d.classList.add('game-topbar__dot--done');
      });
    },
    reset() {
      dots().forEach(d =>
        d.classList.remove('game-topbar__dot--done', 'game-topbar__dot--active')
      );
    }
  };
})();

/* ----- 屏幕切换 -----
   showScreen('level-1')  → 激活 #screen-level-1
   自动滚动到顶部。
----------------------------------------------------- */
function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  const el = document.getElementById('screen-' + id);
  if (el) {
    el.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
