# taiwan_war_simulator

面向 **战争策略回合制游戏** 的 Codex 协作开发骨架。
目标是让 AI 和人类在「规则清晰、数据可调、回放可验」的流程里稳定迭代。

## 目录结构（针对回合制战争策略）

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── design/
│   │   ├── game_design_document.md      # 核心体验、胜负、阵营、资源、回合循环
│   │   └── technical_design.md          # 模块边界、状态机、存档/回放
│   ├── narrative/
│   │   └── worldbuilding.md             # 势力背景、事件线、政治叙事
│   ├── prompts/
│   │   └── codex_prompting.md           # AI 任务模板（系统/战役/AI/数值）
│   ├── tasks/
│   │   └── backlog.md                   # 任务与版本里程碑
│   └── logs/
│       └── devlog.md                    # 每次迭代决策记录
└── tools/
    └── ai/
        └── README.md                    # 内容生成、平衡校验、战报分析脚本
```

## 建议的代码与数据分层（下一步可按此创建）

```text
src/
├── core/             # turn 状态机、事件总线、随机种子
├── campaign/         # 战役进度、胜负结算、章节目标
├── combat/           # 命中/穿甲/士气/地形/补给结算
├── ai/               # 战术 AI、战略 AI、行动评分
├── map/              # 地块、视野、路径、控制区(ZOC)
├── economy/          # 资源、生产、维修、补给线
└── diplomacy/        # 关系、停火、援助、制裁

data/
├── units/            # 单位模板（机动、火力、装甲、补给消耗）
├── factions/         # 阵营属性与科技树
├── scenarios/        # 剧本地图、初始部署、胜负条件
├── balance/          # 版本化平衡参数
└── localization/     # 多语言文本

tests/
├── deterministic/    # 固定 seed 的可复现测试
├── simulation/       # 多回合自动对战回归
└── rules/            # 战斗/补给/胜负规则单测
```

## 开发顺序建议

1. 先填 `docs/design/game_design_document.md` 的「回合循环 + 胜负 + 关键系统」。
2. 再做 `docs/design/technical_design.md` 的「状态流与数据契约」。
3. 通过 `docs/tasks/backlog.md` 拆到可在 1~2 天完成的小任务。
4. 每次规则改动必须补对应测试（至少 deterministic + rules）。
5. 在 `docs/logs/devlog.md` 记录“为什么改、改了什么、结果如何”。
