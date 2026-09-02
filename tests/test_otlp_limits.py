from pathlib import Path

import pytest

from fixbundle.otlp import OTLPError, build_otlp_bundle


def test_otlp_rejects_input_larger_than_configured_bound(tmp_path: Path):
    logs = tmp_path / "logs.jsonl"
    logs.write_text('{"resourceLogs": []}\n', encoding="utf-8")

    with pytest.raises(OTLPError, match="input exceeds"):
        build_otlp_bundle(
            logs_path=logs,
            traces_path=None,
            output_dir=tmp_path / "out",
            max_input_bytes=4,
        )
