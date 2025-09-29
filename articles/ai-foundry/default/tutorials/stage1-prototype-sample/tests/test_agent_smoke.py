"""Placeholder smoke test.
This will not run successfully until SDK imports and environment are verified.
"""
from pathlib import Path

def test_structure_exists():
    assert Path("src/agent_app/config.py").exists(), "config.py missing"
    assert Path("assets/eval_questions.jsonl").exists(), "eval dataset missing"
