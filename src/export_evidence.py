"""합성 관측에서 실제 생성한 분석과 보고서 본문을 내보낸다."""
import json
from pathlib import Path
from .report_demo import build_report, markdown


def build():
    observations = json.loads((Path(__file__).resolve().parents[1] / "examples/observations.json").read_text())
    report = build_report(observations)
    return {"scope": "executed_offline_synthetic_report_not_production",
            "observations": observations, "analysis": report, "markdown": markdown(report)}


if __name__ == "__main__":
    print(json.dumps(build(), indent=2, ensure_ascii=False))
