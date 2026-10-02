# From Public Data to a Reviewed Report

2026-10-02 운영 코드·읽기 전용 SQL 집계·실제 조회 함수를 대조한 기록입니다.
원천 데이터·운영 소스·직원 정보를 공개하지 않고 **집계 관측과 단계별 책임**만 설명합니다.
[집계 JSON](data-inventory-20261002.json)은 운영 관측이며 공개 합성 데모의 fixture가 아닙니다.

## 1. How much data is stored?

수치는 SQL `count(*)`로 확인했습니다. 이력·버전·원문·상세·집계 테이블은 서로 중복될 수 있어
합계를 “고유 데이터 수” 또는 “리포트 한 건이 읽은 양”으로 표현하지 않습니다.
수집 성공 시각, 자료 발행일, 예측 대상일도 서로 다릅니다.

| Source / data family | Tables | Stored rows | Report use / boundary |
|---|---|---:|---|
| KREI 문서·PDF | seed_source_documents / seed_krei_reports | 각각 82 | 버전 행; current 21개, distinct PDF content hash 21개 |
| KREI 페이지·작물 텍스트 | seed_document_pages / seed_krei_crop_texts | 937 / 293 | OCR/텍스트, 작물별 원문·보정·검수 상태 |
| KREI 추출 지표 | seed_krei_forecast_metrics | 1,526 | 면적·의향·출하·생산·단수·가격·수입 등 후보; 전량 승인 아님 |
| aT 시장 가격 | at_price_trend / at_price_regional / at_price_monthly | 76,080 / 567,637 / 3,538 | 품목·품종·등급·단위·지역·기간이 맞는 비교 |
| 공영도매시장 경매 | wholesale_auction_daily | 750,767 | 가격·반입·품종 구성·시장 변화; 마지막 거래일 09-30 |
| 국립종자원 품종보호 / 판매신고 | plant_variety_protection / variety_declaration | 1,246 / 462 | 출원·보호와 생산·수입 판매신고를 구분 |
| 품종 특성 / 종자 공급 | variety_profile / seed_supply_area | 913 / 12,865 | 특성·공급 근거; 공급량을 재배면적으로 바꾸지 않음 |
| 공식 재배 통계 | crop_cultivation_stats | 12,475 | 전국·지역, 연도·작물·작형별 면적/생산 |
| 농작업 단계 / 매뉴얼 | crop_growth_stage / nsr_farm_work_dtl | 4,121 / 176 | 파종·육묘·정식·준비 시점의 기준 |
| 기상청 일 관측 | seed_agri_weather_stations / seed_agri_weather_daily | 97 / 8,982 | 최신 관측 10-01; 과거 관측은 비교 구간이며 연속 5년 전량 적재 아님 |
| 관측소 매핑 / 작물 profile | seed_agri_weather_region_maps / seed_crop_weather_profiles | 101 / 32 | 지역·작물 매핑, 승인 기준온도·가중치; 모든 작물에 적용 가능하다는 뜻 아님 |
| 공식 병해충 회보 | ncpms_bulletin / ncpms_bulletin_alert | 259 / 4,281 | 회보 발행기간·작물·병해충·단계 |
| 예측 지도 / 지역 일별 예보 | ncpms_forecast_map / ncam_pest_forecast_daily | 9,802 / 39,269 | 예측 대상일·지역·작물·병해충·위험단계; 확정 발생률 아님 |
| 병해 / 해충 설명 | ncpms_desease_detail / ncpms_pest_detail | 957 / 611 | 병징·발생환경·생태·피해 설명 |
| 현행 등록정보 | pesticide_info | 134,750 | 동일 작물·병해충의 등록 용도·희석·사용기준 확인 |
| 공공 전문가 상담 | ncpms_consult_detail / nongsaro_consulting / nsr_spt_tchnlgy_sport_view | 5,011 / 1,906 / 1,287 | 현장 사례; 소스 간 중복 가능, 현재 지역 발생 건수로 해석하지 않음 |
| 주간농사정보 | nsr_week_farm_info | 873 | 호수·기간·작물별 현장 점검 사항 |
| 커뮤니티 / 댓글 | agri_community_posts / agri_community_comments | 4,279 / 5,889 | 공공기관 데이터와 구분한 낮은 신뢰의 현장 경험; 개인 원문은 공개하지 않음 |
| 현장 신호 집계 | agri_field_signal_daily_stats | 640 | 언급 빈도·지역·작물·병해충; 실제 발병률 아님 |
| 지원 / 종자 조달 / 기관 소식 | agri_support_programs / seed_procurement_bids / seed_agency_news | 360 / 177 / 85 | 진행 기간·관심 작물·목적에 맞는 공고 선별 |

전국 가격 최신일은 09-30, 지역 가격 10-01, NCAM 예측 대상일은 10-08까지입니다.
KREI 원문 수집 성공은 10-02이지만 현재 자료의 최대 publication_date는 09-02입니다.
“오늘 수집 성공”을 “오늘 발표된 최신 자료”로 표시하지 않습니다.

## 2. Storage is not report eligibility

이번 관측에서 확인한 실제 KREI 선택 경로입니다.

```text
82 document/version rows (21 distinct content hashes)
  → 937 page rows / 293 crop-text rows / 1,526 metric candidates
  → metric status alone: 682 AUTO_VALIDATED or APPROVED
  → current-version metrics: 404 (different filter, not a subset of the 682)
  → current report + permitted report status + permitted metric status: 0
```

현재 current 보고서 21개가 모두 `REVIEW_REQUIRED`입니다. 정형 조회는 상위 보고서 상태도
검사하므로 검증 지표가 저장돼 있어도 선택되지 않습니다. 검수·버전 전환 운영을 점검할
후속 과제이며, 이번 공개 작업에서 승인 상태를 자동으로 바꾸거나 gate를 완화하지 않았습니다.
정성 전망은 별도의 페이지 원문 fallback을 사용하므로 정형 지표 0건과 같지 않습니다.
원문 fallback은 승인된 정형 수치나 관리자 승인문으로 승격하지 않습니다.

## 3. Pipeline and intermediate artifacts

| Stage | Input and processing | Intermediate result | Next-stage boundary |
|---|---|---|---|
| Acquire | 공식 API/XML/JSON, PDF 목록/다운로드, 공개 게시판, 선택형 웹 보완 | 원문 payload, source ID/URL, 수집·자료 시각 | 출처·권리·수집 상태 보존; 기업 내부 상담은 공개 근거에서 제외 |
| Version & parse | 원문 hash/current version, PDF 텍스트 추출; 품질 부족 시 OCR | 문서 버전, page_text, OCR 여부, 페이지 품질 | 과거 버전과 current를 구별; OCR 사용 자체가 정확성 보증은 아님 |
| Normalize | URL/HTML 해제, OCR 글줄 재구성·노이즈 정리, 작물·지역·단위·시점 분리 | 작물별 원문, 정형 지표 후보, source_page/source_quote | 동명이칭·배/배추 같은 부분 일치와 지표 혼동 방지 |
| Review | PDF 이미지와 원문을 통한 LLM 보정, 검수·제외·승인 | raw/refined/manual text, review status, approved-text hash | 미승인 보정문을 승인문으로 취급하지 않음; 원문 변경 시 재검수 |
| Select | 관심 작물·지역·시기·정렬·상한·검수 gate | 보고서 전용 evidence bundle | 누락·0건·fallback을 남김; 전체 DB를 prompt에 투입하지 않음 |
| Calculate | 가격/반입 비교, 단위 정합성, 예보 달력, 적산온도, 공식 재배 통계 | 시장 신호·수요 준비기간·기회 후보·근거 ID | 계산 결과와 해석을 분리; 가격 상승만으로 수요 확정 금지 |
| Compose | 섹션별 LLM 편집·근거 요약·종합 브리핑 | 섹션 문장, 요약, 사용/실패 상태 | 원천 등록 수치·면적·출처 범위를 보존; LLM 문장이 승인 사실은 아님 |
| Render | 작물보호제/종자별 독립 builder | HTML/text, CID 이미지, 종자 상세 PDF, summary/quality | 미리보기와 실제 발송을 구별 |
| Validate & review | 항목·길이·첨부·근거·LLM 검토, 정책별 사람 승인 | score/checks/warnings, ready/needs_review/approval_pending | 내부 점수는 정확도나 사업 성과가 아님 |
| Persist & deliver | 구현된 payload pack/hash와 staged delivery | 압축 artifact, 수신자 snapshot, 발송 이력 | 개인 식별 정보는 비공개; 이번 조회의 artifact 테이블은 0행이므로 운영 사용 실적을 주장하지 않음 |

공개 repo는 위 운영 소스의 복사본이 아닙니다. 현재 재현 가능한 공개 코드는 합성 입력의
정형 비교·근거 연결·렌더링입니다. 실제 LLM/수집/발송 경로는 검토 증거로 설명합니다.

## 4. What did actual retrieval select?

2026-10-02, 공개 예시 맥락 **벼·수박·참외·양파·무 / 경북·전남·강원·제주·경남·전북**으로
기존 builder의 읽기 전용 조회 함수를 직접 실행했습니다. 직원 계정·개인 선호는 조회하지 않았습니다.
이는 **선택 단계 측정**이며 새 리포트 생성, 실제 LLM 소비량, 최종 인용량 측정이 아닙니다.

| Selected output | Actual result | Meaning |
|---|---:|---|
| KREI 정형 지표 | 0 | 현재 버전·검수 gate에 의해 제외 |
| KREI 정성 전망 | 3 | 페이지 원문 fallback을 포함한 작물 전망 묶음 |
| 가격 | 5작물 | 모두 가격 데이터 존재; 내부 비교 행 수와 구분 |
| 경매 신호 | 4작물 | crop-level aggregation; 750,767행 전체가 prompt에 들어간 것이 아님 |
| 품종보호 / 판매신고 | 25 / 18 | 선택·정렬·제외 규칙 후 결과 |
| 공식 재배 통계 | 105행 | 선택 작물·지역의 통계 근거 |
| 농업기상 | 30 작물×지역 신호 | GDD 값 18개, 승인 profile 부재 12개; 신뢰도 0.65 미만 5개 |
| 종자용 관심작물 위험 예보 | 0 | 선택 5작물은 관측한 최근 NCAM 작물 범위와 불일치; 전국 예보 부재 아님 |
| 작물보호제 NCAM | 249행 → 18 지역×작물 그룹 → priority 16 | 해당 경로는 지역 최대 3곳 적용: 경북·전남·강원 |

최근 NCAM에 있는 작물은 배·감귤·고추·사과·포도·복숭아였습니다.
0건은 source 고장, 데이터 없음, 필터 불일치, 승인 대기를 구별해야 합니다.
전체 fetch→LLM payload→최종 인용의 run별 공통 manifest는 후속 보완 항목입니다.

## 5. Degree-day calculation and report interpretation

일 적산온도는 `max(0, min(Tmean, upper) - Tbase)`입니다. upper가 없으면 상한을 적용하지 않고,
평균기온이 없을 때만 최저·최고 평균으로 대체합니다. 승인된 작물 profile을 사용하며
동일 관측소의 최근 28일과 과거 동일 기간(가용 최대 5년) 중앙값을 비교합니다.
일사량 coverage·과거 비교 가능 연수로 신뢰 수준을 계산하고, 0.65 이상일 때만 준비일 보정을 적용합니다.
이 값은 **환경 진행의 보조 지표**이며 실제 파종일·주문 확정일·수확일 예측 정확도가 아닙니다.
전체 관측소가 모든 과거 날짜를 보유하는 것도 아닙니다.

[지역별 적산온도 화면](screenshots/seed-growing-degree-days.png)은 무·벼와 함께,
승인 profile이 없는 양파의 GDD 미표시 상태도 그대로 보존합니다.

## 6. Validation findings, not hidden success claims

이번 선택 private reporting suite는 **243 passed / 2 failed**였습니다. 공개 25개 테스트와
별도입니다. 실패는 현장 신호 SQL 결과의 7열 계약과 구형 6열 fixture 불일치,
품종 편집 prompt의 기대 문구 불일치입니다. 운영 성능 평가 결과로 사용하지 않습니다.

추가로 실제 한글화 함수가 바꾼 두 섹션 제목을 품질 gate가 옛 문자열로 검사하는 불일치를
재현했습니다. 표시문구가 아니라 안정적인 section ID로 검사하는 방향이 필요합니다.
KREI 검수 흐름, 이 제목 계약, run별 근거 사용 manifest, 독립 보고서 품질 평가가 남아 있습니다.
저장된 인사이트의 좁은 표에서는 일부 한글이 겹치는 표시 문제도 보여 반응형 표 검증이 필요합니다.
이번 공개 문서·화면 보완에서 운영 승인·수집·발송 로직은 변경하지 않았습니다.
