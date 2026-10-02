# Data & Workflow Evidence

2026-10-02 현재 report builders, seed source API, KREI review API, 관리 UI를 대조했습니다.
오래된 설계 문서보다 현재 조회 조건·검수 상태·화면을 우선했습니다.

추가 감사: [실제 적재량·선택량·단계별 산출물](data-to-report.md)을 SQL 집계와 기존 조회 함수로 확인했습니다.
현재 KREI 정형 입력 0건과 별도 정성 fallback, 제목 정규화/품질 gate 불일치,
private 선택 회귀 243 통과·2 실패를 기록했습니다. 아래의 기능 구현 설명이 모든 경로의 운영 성공을 뜻하지 않습니다.

## Data Sources & Tables

| 영역 | 실제 테이블 / 자료 | 리포트에서의 역할 |
|---|---|---|
| KREI 원문 | seed_source_documents, seed_document_pages, seed_krei_reports | 문서 버전·페이지·관측호 |
| KREI 텍스트 | seed_krei_crop_texts | 추출본·Qwen 보정본·관리자 최종본·승인 hash |
| KREI 정형 사실 | seed_krei_forecast_metrics | 재배의향·정식·재배·출하 등 지표별 근거 |
| 시장 가격 | at_price_trend | 작물별 시점·단위·증감 비교 |
| 품종 | variety_profile, seeds_products | 품종 특성·제품 근거 |
| 공급 | seed_supply_area | 종자 공급 신호; 재배면적과 구분 |
| 생육 일정 | crop_growth_stage | 파종·육묘·정식 상담 시기 |
| 지원사업 | agri_support_programs | 종자·묘·작목전환 등 관련 지원 |
| 기상 | seed_agri_weather_stations / daily / region_maps | 관측소·지역·일별 관측 |
| 소스 운영 | seed_data_sources | 수집 주기·상태·성공 시점 |
| 실행 결과 | seed_sales_opportunities / seed_weekly_preferences | 기회 점수·개인화 |

데이터 연결 화면에는 주간농사정보, KAMIS, 실시간 경매, KOSIS, 국립종자원 품종보호·판매등록,
전문가·커뮤니티 현장 신호, 지역 병해충 예보, 지원·조달, 공간정보도 구분되어 있습니다.
'연결됨'은 모든 source가 적재 완료라는 뜻이 아닙니다. 중지·미수집 상태도 그대로 표시합니다.

## Actual KREI Processing

목록 / PDF → 문서 hash·버전 → 페이지 텍스트/OCR → 작물별 결합
→ Qwen PDF-image 보정 → 관리자 텍스트 검수 → 보고서 입력.

현재 정형 조회는 AUTO_VALIDATED / APPROVED 수치와 유효한 current report 및 상위 검수 상태를 함께 검사합니다.
이번 실제 관측에서 current 21개 보고서가 REVIEW_REQUIRED여서 정형 입력은 0건이었습니다.
텍스트는 승인본과 보정본의 출처 상태를 보존하며 승인 hash가 달라진 텍스트는 제외합니다.
모든 자료가 사람에게 승인된 것처럼 표현하지 않습니다.
9월호 검수 캡처는 2026년 9월 과일관측의 REVIEW_REQUIRED 상태입니다.

## Report Builders

작물보호제 빌더는 지역·작물별 데이터, 날씨·웹 보완, LLM 섹션 정리와 종합 인사이트, 품질 검사, HTML을 생성합니다.
종자 빌더는 별도 수요/시장/품종 관점과 개인화·품질 기준을 사용하고 예약·artifact·발송 운영 기반은 공유합니다.

정형 계산과 LLM 설명의 책임을 구분하고 숫자·공급량·면적의 의미 차이를 유지합니다.
원문 전체를 무조건 최종 prompt에 넣기보다 목적별로 조회·정리해 사용합니다.

## Screen Provenance

현재 소스 연결과 KREI 검수는 1920×1080 브라우저에서 실제 읽기 전용 API로 새 촬영했습니다.
리포트 화면은 이미 저장된 실제 생성 HTML 또는 승인된 미리보기 캡처를 재사용했습니다.
새 리포트 생성·직원 수정·발송은 실행하지 않았습니다.
과거 HTML의 빈 KREI 섹션은 현재 통합 근거로 채택하지 않고 실제 값이 있는 시장 섹션을 선정했습니다.

추가 예보·적산온도 캡처는 현재 DB와 기존 섹션 렌더러를 연결한 읽기 전용 검증입니다.
종자 인사이트는 2026-09-02 저장본을 발췌했고 새 전체 보고서 생성본으로 표시하지 않습니다.
