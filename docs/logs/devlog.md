# Dev Log

## Entry Template

Use this template for every notable change:

```text
## YYYY-MM-DD
### Short Title
- Why: why the change was needed.
- What Changed: the concrete updates that were made.
- Result: the observed outcome, verification status, or follow-up impact.
```

## 2026-03-31
### Turn-Based Strategy Scaffold
- Why: The repository needed an initial structure aligned to a turn-based war strategy game instead of a generic project template.
- What Changed: Adjusted the scaffold, clarified the core turn loop as intel -> orders -> resolution -> end of turn, and added constraints covering supply, morale, zones of control (ZOC), and deterministic replays.
- Result: The project now has a clearer design direction and a rules-first workflow for future implementation.

## 2026-03-31
### Backlog and Rule-Test Workflow
- Why: The original backlog was too coarse to support 1 to 2 day implementation slices, and the testing/devlog expectations needed to be explicit before rule work begins.
- What Changed: Split the backlog into smaller module-grouped tasks, added an explicit requirement for deterministic and rules coverage on rule changes, reinforced the workflow in the design docs and README, and standardized the devlog entry format.
- Result: The planning docs now support incremental delivery with clearer acceptance criteria, test expectations, and decision logging.

## 2026-03-31
### Playable CLI Prototype v0.2
- Why: 现有仓库只有文档框架，尚不可直接游玩，无法进行回合体验与规则验证。
- What Changed: 新增 `twsim` 可执行原型（行动选择、AI 响应、事件结算、阶段推进、终局判定），补充 `pytest` 测试基线，并新增 deterministic/rules 测试覆盖可复现性与关键阈值规则；同步更新设计文档与 backlog 状态。
- Result: 仓库现在可通过命令行直接进行 20 天回合制对局，并可通过自动化测试验证规则正确性与可复现性。

## 2026-03-31
### Narrative Background Pack
- Why: 现有叙事文档仍是占位内容，无法为台海危机场景提供可直接用于系统设计的背景支撑。
- What Changed: 重写 `docs/narrative/worldbuilding.md`，并新增 `docs/narrative/prc_resource_pool.md` 与 `docs/narrative/strategic_variable_matrix.md`，将中方资源层级、危机节奏与决定战局的关键变量压缩为适合游戏抽象的简明文档。
- Result: 叙事层现在可直接支撑行动设计、事件池编写与阶段扩展，同时避免把原型误导成纯编制表或纯登陆战模拟。

## 2026-03-31
### Taiwan Background Pack
- Why: 台湾阵营仍缺少与中方文档对称的背景拆分，现有资料不足以支撑对手行为、韧性事件和防御节奏设计。
- What Changed: 新增 `docs/narrative/taiwan_resource_pool.md` 与 `docs/narrative/taiwan_defense_variables.md`，并在 `docs/narrative/worldbuilding.md` 中补全双方资料索引，将台湾资源层、拒止逻辑、全民动员与关键防御变量压缩成适合游戏使用的简明文档。
- Result: 叙事资料现在同时覆盖攻方与守方两侧，为后续扩展 AI 行为、事件池和阵营参数表提供了统一入口。

## 2026-03-31
### Foreign Intervention Pack
- Why: 现有叙事资料仍缺少第三方介入这一关键层，无法支撑联盟升级、基地开放、后勤支援与多战区牵制相关设计。
- What Changed: 新增 `docs/narrative/foreign_intervention_pool.md` 与 `docs/narrative/foreign_intervention_variables.md`，并在 `docs/narrative/worldbuilding.md` 中补充对应索引，将美国、区域盟友、欧洲支持与俄朝牵制压缩为适合游戏建模的资源层与变量表。
- Result: 项目现在具备攻方、守方和第三方三侧背景骨架，可继续拆分为介入等级、基地开放度、联盟协调与制裁系统。

## 2026-03-31
### Scenario Content Pass
- Why: 虽然背景骨架已经补齐，但原型内容层仍接近占位状态，行动、事件与对手反馈还不足以体现台海危机的真实博弈结构。
- What Changed: 扩充 `src/twsim/content.py` 中的行动池、事件池与终局描述，加入封港、联合火力、无人机袭扰、民船征用、法理通告、市场稳定等内容；同时为 AI 响应补充本地化标签，并在测试中锁定扩充后的行动规模与日报文本表现。
- Result: CLI 原型现在能更直接体现中方施压、台湾韧性与外国干涉的多层互动，回合反馈也比原先更贴近场景设定。

## 2026-04-01
### Visual Prompt Export for Pixel-Style Realtime Rendering
- Why: 需要把“Flash 感实时 2D 像素风 + 选项前后持续反馈动画”的视觉要求沉淀为可复用的统一提示词，供前端、美术与工具链一致使用。
- What Changed: 新增 `src/twsim/visual_style.py` 输出标准化视觉提示词；CLI 增加 `--visual-style-prompt` 导出入口；补充对应测试验证提示词关键约束与命令行输出；README 增加使用说明。
- Result: 项目现在可一键导出统一视觉规范文本，确保地图/单位/UI 分层、行动动画链路与交互反馈要求在协作中保持一致。
