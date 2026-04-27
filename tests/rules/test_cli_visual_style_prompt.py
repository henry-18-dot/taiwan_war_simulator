from __future__ import annotations

from twsim import cli


def test_cli_visual_style_prompt_prints_and_exits(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["twsim", "--visual-style-prompt"])
    cli.main()
    captured = capsys.readouterr()
    assert "游戏视觉与渲染风格提示词" in captured.out
    assert "实时渲染" in captured.out
