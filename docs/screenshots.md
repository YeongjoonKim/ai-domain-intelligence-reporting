# Reporting Evidence Gallery

## Added: Forecast, Degree Days and Insight

| Image | Data / capture provenance | Boundary |
|---|---|---|
| [지역·날짜별 병해충 예보](screenshots/protection-forecast-regions.png) | 2026-10-02 읽기 전용 NCAM 조회 166행, 경북·전남, 기존 섹션 렌더러 | 새 전체 보고서 생성/발송 아님; 11일 표시 창의 미적재 날짜 유지 |
| [일사량·적산온도](screenshots/seed-growing-degree-days.png) | 같은 날짜의 무·벼·양파 × 경북·전남 6개 신호, 기존 섹션 렌더러 | 승인 profile 없는 GDD는 미표시; 보조 환경 신호 |
| [종자 인사이트 첫 부분](screenshots/seed-insight-opening.png) | 2026-09-02 저장 HTML의 기존 브리핑 상단만 발췌 | 과거 생성문, 현재 DB/새 LLM 출력과 구분 |

회사명·직원 이름·이메일이 없는 섹션만 선택했습니다. 원문은 보존하고 픽셀 사본은 metadata 없이
평탄화했습니다. 예보/적산온도는 화면 안에도 섹션 재렌더링임을 명시했습니다.
계정 로그인·운영 상태 변경·새 LLM 호출·발송 없이 격리된 브라우저로 확인했고 JS 오류는 없었습니다.
적산온도 캡처는 수치·신뢰도 부분이며 지도/chart 이미지 전체를 캡처한 것은 아닙니다.

[데이터 규모와 단계별 처리](data-to-report.md)에서 저장량·선택량·최종 사용량의 차이를 설명합니다.

## Actual reports & source management

### Seed Report Preview

**Purpose** — 지역·작물별 검토 기회와 근거 부족 상태를 확인합니다.

![Actual seed preview](screenshots/seed-report-preview.png)

**What this demonstrates** — 2026-08-04 저장된 실제 HTML의 리포트 첫 화면. 직원 식별 영역을 마스킹했습니다.
**Architecture relation** — Analysis → Report → Review.

### Seed Market

**Purpose** — 단위와 비교 시점을 유지한 시장 정보를 확인합니다.

![Actual seed market section](screenshots/seed-report-market.png)

**What this demonstrates** — 2026-07-31 가격 및 전주·전년 비교를 표시한 과거 생성 결과.
**Architecture relation** — Structured Market Data → Report.

### Seed Calendar

**Purpose** — 생육 달력 데이터를 종자 상담 자료에 연결한 출력 형식을 확인합니다.

![Actual seed calendar section](screenshots/seed-report-calendar.png)

**What this demonstrates** — 저장된 리포트의 달력 섹션. 이 과거 화면은 1월 설명을 표시하므로 생성 월의 적시성 검증 자료로 사용하지 않습니다.
**Architecture relation** — Crop Calendar → Report Section.

### Crop Protection Preview

**Purpose** — 관심 작물·지역과 병해충 정보를 조합한 미리보기를 검토합니다.

![Actual crop protection preview](screenshots/protection-report-preview.png)

**What this demonstrates** — 2026-07-28 생성된 보고서의 첫 화면. 이름·소속·직급을 마스킹했습니다.
**Architecture relation** — Pest / Regional Signals → Report.

### Weather Section

**Purpose** — 지역별 관측과 시간대별 예보의 전달 방식을 확인합니다.

![Actual report weather section](screenshots/protection-report-weather.png)

**What this demonstrates** — 위 과거 리포트의 서울 날씨·시간대별 예보 표.
**Architecture relation** — Weather Data → Regional Report.

현재 [데이터 연결 현황](screenshots/seed-source-connections.png)과
[9월 KREI 검수](screenshots/krei-september-review.png)는 2026-10-02 새 캡처입니다.
과거 리포트와 현재 운영 관리 화면의 시점을 구분합니다.

## Operational screenshots

기존 관리자 화면을 크롭하고 필요한 식별 영역만 불투명 마스킹한 승인 사본입니다.
원본은 보존하며 UI 수치·상태·본문을 합성 값으로 바꾸지 않았습니다.

| 화면 | 사본 | 보여주는 것 / 한계 |
|---|---|---|
| 발송 설정 | [보기](screenshots/admin-schedule.png) | 사전 생성·품질 기준·승인 옵션; 실제 배달 성공 증거 아님 |
| 수집 자료 검토 | [보기](screenshots/admin-source-review.png) | AUTO_PARSED / REVIEW_REQUIRED, 수정 승인·제외; 값은 미확정 추출 후보 |
| 보고서 미리보기 | [보기](screenshots/admin-report.png) | 지역·작물 관심에 따른 과거 보고서; 내부 점수는 정확도 benchmark 아님 |

계정 목록과 회사 표시는 화면 밖으로 제외했습니다.
보고서의 직원 이름·이메일·소속·직급은 단색 픽셀로 덮고 metadata 없는 PNG로 평탄화했습니다.
파일 안에 복구 가능한 원문 레이어를 넣지 않았습니다. 이 자료로 최신 발생 현황을 주장하지 않습니다.

## Public Execution

아래는 관리자 서비스가 아닌 **공개 예제의 실제 실행 결과 문서**를 Chrome으로 캡처한 것입니다.
[JSON](../examples/execution.json) → [HTML](../examples/execution.html)을
[renderer](../src/render_evidence.py)가 생성하며 회귀 테스트가 저장본과 재실행을 비교합니다.

- [입력 계약](screenshots/inputs.png): origin·단위·기간을 유지하는 합성 관측.
- [분석](screenshots/analysis.png): 실제 Decimal 비교와 이력 부족 상태.
- [생성 보고서](screenshots/report.png): template 출력이며 LLM 결과가 아님.

[캡처 hash](screenshots/manifest.json)는 두 종류의 공개 파일을 식별합니다.
운영 캡처와 합성 결과를 같은 실행이나 같은 성과로 연결하지 않습니다.
