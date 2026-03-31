# Codex Prompting（战争策略回合制）

## 通用任务模板
```text
目标：
游戏阶段：战略层 / 战术层 / 结算层
修改范围：
输入文档：
输出文件：
验收标准：
确定性要求：同 seed + 同 action 序列结果一致
```

## 示例 1：补给线规则
```text
目标：实现“补给线中断惩罚”
游戏阶段：结算层
修改范围：只改补给结算模块与对应 tests
输入文档：docs/design/game_design_document.md
输出文件：src/economy/*, tests/rules/*
验收标准：
1) 无补给连续 2 回合后机动 -30%
2) 连续 3 回合后火力 -20%
3) 测试覆盖边界条件
```

## 示例 2：战术 AI 行动评分
```text
目标：提高 AI 对关键据点的争夺优先级
游戏阶段：战术层
修改范围：src/ai/tactical/*
输入文档：docs/design/game_design_document.md, docs/design/technical_design.md
输出文件：src/ai/tactical/*, tests/simulation/*
验收标准：100 局模拟中关键据点占领率提升且胜率不过拟合
```
