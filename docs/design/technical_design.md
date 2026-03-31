# Technical Design (Turn-based Simulation)

## 1) Simulation architecture
- `TurnState`: 当前回合的完整状态快照
- `ActionQueue`: 指令阶段收集的玩家/AI动作
- `Resolver`: 按固定顺序结算动作与冲突
- `EventLog`: 记录每次状态变化（支持回放/调试）

## 2) Determinism requirements
- 所有随机数由统一 `seed` 和回合编号驱动
- 结算顺序稳定（同优先级按固定规则排序）
- 浮点计算尽量离散化或统一精度策略

## 3) Data contracts
- 单位配置：`data/units/*.json`
- 地形配置：`data/scenarios/*/terrain.json`
- 战斗参数：`data/balance/combat.json`
- 胜负条件：`data/scenarios/*/victory.json`

## 4) Testing strategy
- `tests/rules`: 规则单测（命中/穿甲/补给）
- `tests/deterministic`: 固定 seed 回归
- `tests/simulation`: 多回合自动对战监控平衡漂移
