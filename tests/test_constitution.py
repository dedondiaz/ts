from pathlib import Path

import pytest

from aicorp.constitution import ConstitutionError, load_constitution


def test_load_constitution_success():
    path = Path(__file__).resolve().parents[1] / "aicorp" / "constitution.json"
    constitution = load_constitution(path)
    assert constitution.version == "0.1"
    assert "simulator.run" in constitution.tool_allowlist


def test_load_constitution_missing_field(tmp_path: Path):
    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{}")
    with pytest.raises(ConstitutionError):
        load_constitution(bad_path)
