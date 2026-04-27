from __future__ import annotations

from twsim.visual_style import visual_style_prompt


def test_visual_style_prompt_has_required_feedback_guards():
    prompt = visual_style_prompt()
    assert "选择选项时必须有动作反馈" in prompt
    assert "选择选项后必须有确认反馈与持续动画" in prompt
    assert "地图 > 单位 > UI" in prompt


def test_visual_style_prompt_has_core_animation_examples():
    prompt = visual_style_prompt()
    assert "攻击 -> 像素爆闪 + 数值弹出" in prompt
    assert "占领 -> 区域颜色渐变填充" in prompt
    assert "移动 -> 路径线 + 单位逐格移动" in prompt
