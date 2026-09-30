# AI Decision Support & Domain Intelligence Reporting

## 01 Overview

An offline pipeline turns invented dated observations into an evidence-linked Markdown brief. It validates origin and units, computes Decimal changes and preserves unresolved cases. **12 behavioral tests** exercise the contracts. No live LLM, collection service or business forecast runs here.

This repository is a sanitized and reconstructed technical showcase based on engineering experience from a private production AI platform.
It does not contain proprietary source code, private data, internal APIs, or production configuration.

본 저장소는 비공개 운영 AI 시스템의 설계·개발 경험을 기반으로 독립 재구성한 공개 기술 예제입니다. 회사 소스, 비공개 데이터, 내부 API 및 운영 설정은 포함하지 않습니다.

## 02 Problem

Mixed sources can describe different units, periods or metrics. A fluent report can conceal these mismatches. Arithmetic and evidence identity should survive narration.

## 03 Architecture

![Reference architecture](docs/architecture/01_reporting_architecture.svg)

[Editable Mermaid and diagram scope](docs/architecture/README.md).
Statuses are **IMPLEMENTED / PARTIAL / PROPOSED**; synthetic/mock describes the
dependency or data, not an additional implementation status.

## 04 Key Engineering Decisions

Validate synthetic origin, dates, identifier shape and finite values before analysis. Use Decimal and separate metric/unit groups. Mark conflicting periods unresolved instead of choosing a convenient row.

[Design decisions](docs/design-decisions.md).

## 05 Implementation

IMPLEMENTED: synthetic schema/origin checks, date validation, Decimal changes, unit grouping, conflict detection and evidence IDs. PARTIAL: exact structured-projection guard, not free-form prose verification. PROPOSED: public connectors, scheduled automation, LLM insight generation and admin configuration. Narration is currently a deterministic template.

The LLM's intended role is explanation of validated observations, not invention of indicators. A changed index suggests a question to investigate, not an opportunity ranking or commercial recommendation.

## 06 Example

A fictional survey index changes from 80 to 92: +12 points, +15%. Other examples show decline and insufficient history. These are not real prices.

[Example instructions](examples/README.md).

## 07 Evaluation

12 behavioral tests plus five repository-quality checks run without models,
network or GPU. Counts are regression coverage, not model-quality scores.
[Evaluation](docs/evaluation.md) · [Local validation](docs/validation.md).

## 08 Failure / Limitations

No live collection, scheduler, LLM, admin settings service or forecast exists. A zero baseline has undefined percent change. The projection guard checks exact structured insight objects, not free-form prose.

[Failure boundaries](docs/limitations.md).

## 09 Reproducibility

Default sample: Python 3.10+ standard library; no package install, credentials or service
required. Run from the repository root. Synthetic inputs and explicit logic support
local comparison, not reproduction of a private platform.
[Maintenance](docs/maintenance.md).

## 10 Repository Structure

- `src/`: independently written sample modules.
- `examples/`: synthetic inputs or invocation guide.
- `tests/`: behavior and repository-quality regression tests.
- `docs/`: architecture, decisions, evaluation and limitations.
- `scripts/` and `.github/`: local checks and CI configuration.

## 11 Quick Start

```sh
python3 -m src.report_demo
python3 -m unittest discover -s tests -v
python3 scripts/check_repository.py
```

CI targets Python 3.10 and 3.12. Hosted runs are pending publication.

## 12 Research Relevance

Evaluate temporal correctness, source reliability and useful evidence-grounded prose against independent human judgments. No customer model, business rules or original reports are included.

MY CONTRIBUTION: author-confirmed engineering work. PLATFORM CONTEXT: private workflows
described conceptually. PUBLIC RECONSTRUCTION: this independent example.
FUTURE RESEARCH: unimplemented evaluation and integrations.

[Publication review](PUBLICATION.md) · [License notice](LICENSE-NOTICE.md) ·
[Security](SECURITY.md). No open-source license has been selected.
