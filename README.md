# taiwan_war_simulator

一个可迭代的**回合制战争策略原型**仓库，当前已提供可运行的 CLI 可玩版本（`Prototype v0.2`）。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
python -m twsim.cli
```

> 游戏是确定性的：相同 seed + 相同行动序列，会得到相同结果。

## 当前可玩内容（v0.2）

- 每天 1 回合，默认 20 天。
- 每回合固定 3 个行动槽位：
  - `primary`
  - `secondary`
  - `info`
- 系统自动执行：
  - AI 响应
  - 当日系统结算
  - 事件触发
  - 胜负检查
- 支持 6 种终局：
  - 威慑达成
  - 高成本达成
  - 冻结优势
  - 国际失控升级
  - 内部承压失衡
  - 战略失效

## 测试

```bash
pytest
```

测试结构：
- `tests/deterministic/`：可复现与回放一致性
- `tests/rules/`：规则阈值、组合合法性和终局判定
