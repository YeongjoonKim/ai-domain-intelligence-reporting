"""합성 시계열의 검증·정규화·비교·보고를 수행하는 독립 예제다."""

from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import re
from pathlib import Path

FIELDS = {"id", "item", "metric", "unit", "period", "value", "synthetic"}


def normalize(rows, as_of):
    reference = date.fromisoformat(as_of)
    valid, rejected, seen = [], [], set()
    for position, row in enumerate(rows):
        try:
            if not isinstance(row, dict) or set(row) != FIELDS or row["synthetic"] is not True:
                raise ValueError("schema_or_origin")
            if any(not isinstance(row[k], str) or not row[k] for k in FIELDS - {"synthetic"}):
                raise ValueError("field_type")
            if any(not re.fullmatch(r"[a-z][a-z0-9_-]{0,39}", row[k])
                   for k in ("id", "item", "metric", "unit")):
                raise ValueError("invalid_identifier")
            if row["id"] in seen:
                raise ValueError("duplicate_id")
            seen.add(row["id"])
            value = Decimal(row["value"])
            if not value.is_finite() or value < 0:
                raise ValueError("invalid_value")
            if date.fromisoformat(row["period"]) > reference:
                raise ValueError("future_observation")
            valid.append(dict(row, value=value))
        except (ValueError, InvalidOperation, TypeError, KeyError):
            # 원본 레코드나 예외 메시지를 보고서로 전파하지 않는다.
            rejected.append({"row": position, "status": "rejected"})
    return valid, rejected


def build_report(rows, *, as_of="2030-02-28"):
    valid, rejected = normalize(rows, as_of)
    groups = defaultdict(list)
    for row in valid:
        groups[(row["item"], row["metric"], row["unit"])].append(row)
    insights = []
    for (item, metric, unit), records in sorted(groups.items()):
        ordered = sorted(records, key=lambda r: (r["period"], r["id"]))
        periods = [r["period"] for r in ordered]
        if len(periods) != len(set(periods)):
            insights.append({"item": item, "metric": metric, "unit": unit,
                             "status": "conflicting_period", "evidence": []})
            continue
        current = ordered[-1]
        state = {"item": item, "metric": metric, "unit": unit,
                 "status": "insufficient_history", "evidence": [current["id"]],
                 "latest_period": current["period"], "latest_value": str(current["value"])}
        if len(ordered) >= 2:
            previous = ordered[-2]
            change = current["value"] - previous["value"]
            percent = None if previous["value"] == 0 else (change / previous["value"] * 100)
            state.update(status="compared", previous_period=previous["period"],
                         delta=str(change), percent=None if percent is None else str(round(percent, 2)),
                         evidence=[previous["id"], current["id"]],
                         signal="increase" if change > 0 else "decrease" if change < 0 else "unchanged")
        insights.append(state)
    return {"disclosure": "Reconstructed Public Demo", "as_of": as_of,
            "data_origin": "synthetic", "insight_engine": "deterministic_template_not_llm",
            "insights": insights, "rejected": rejected,
            "limitation": "Observed change is not a forecast or a business recommendation."}


def grounded_projection(proposal, report):
    """LLM 연결 지점에서는 구조화된 사실 투영만 허용하며 자유 문장 진실성을 보장하지 않는다."""
    if not isinstance(proposal, list):
        return False
    allowed = report["insights"]
    return all(isinstance(claim, dict) and claim in allowed for claim in proposal)


def markdown(report):
    lines = ["# Synthetic Domain Brief", "", "**Reconstructed Public Demo · not operational data**", "",
             "As of: " + report["as_of"], "", "## Evidence-backed observations", ""]
    for insight in report["insights"]:
        # 합성 ID/지표만 다루며 실행 가능한 HTML을 생성하지 않는다.
        label = json.dumps({k: insight[k] for k in ("item", "metric", "unit")})
        lines.append("- " + label + ": " + insight["status"])
        if insight["status"] == "compared":
            percent = insight["percent"] if insight["percent"] is not None else "undefined (zero baseline)"
            lines.append("  - Change: " + insight["delta"] + "; percent: " + percent)
        lines.append("  - Evidence: " + ", ".join(insight["evidence"]))
    lines += ["", "## Opportunity / risk interpretation", "",
              "An increase is a candidate for investigation, not a sales decision.",
              "Missing history, unit differences and conflicting periods remain unresolved.",
              "", "## Limitations", "", report["limitation"],
              "Narration is a template. No LLM, external API, prices or customer records are used."]
    return "\n".join(lines)


if __name__ == "__main__":
    data = json.loads((Path(__file__).parents[1] / "examples/observations.json").read_text())
    print(markdown(build_report(data)))
