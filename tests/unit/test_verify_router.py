"""Tests for verify-router.py."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_verify_router():
    import importlib.util

    path = ROOT / "scripts" / "verify-router.py"
    spec = importlib.util.spec_from_file_location("verify_router", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_extract_test_command():
    mod = _load_verify_router()
    card = """
# Task 001: Smoke

## Test command

`python -c "print(1)"`
"""
    section = mod.extract_section(card, "test command")
    cmd = mod.extract_command(section)
    assert cmd == "python -c \"print(1)\""
