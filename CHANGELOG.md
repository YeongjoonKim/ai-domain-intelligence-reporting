# Changelog — Data Provenance & Human Validation

## 2026-10-02 — Technical portfolio polish

- Data & Workflow Facts와 데이터→분석→검수→리포트 흐름을 상단에 정리했다.
- 작물보호제·종자 화면을 앞세우고 데이터 규모·중간 산출물·검수 과제의 근거를 유지했다.
- 세부 예제 수치는 평가 문서로 옮기고 화면 설명을 한국어로 통일했다.

## 2026-10-02 — Data-to-report evidence expansion

- 40개 관련 테이블의 읽기 전용 행 집계와 source/version/eligibility 차이를 추가했다.
- 실제 조회 함수의 선택량, 전처리·중간 산출물·품질/발송 경계를 단계별로 연결했다.
- 예보 날짜/지역, 적산온도, 저장된 종자 인사이트 첫 부분의 비식별 화면 3개를 추가했다.
- KREI current 검수 gate, 제목 계약 불일치, 기존 회귀 2건 실패를 후속 과제로 명시했다.
- 공개 집계 계약 테스트 3개를 추가했다. 운영 생성/승인/발송 로직은 변경하지 않았다.

## 2026-10-02 — Portfolio hardening

- Source Version → Extraction → LLM Refinement → Human Validation → Structured Fact → Report 관계를 명시하고 supporting evidence project로 역할을 정리했다.
- 저장소별 publication, security, rights 경계를 개별화했다.
- 기존 공개 이력과 실제 화면을 유지하며 과거 개발일이나 평가 결과를 소급 생성하지 않았다.

## Existing public package

독립 예제, 회귀 검사, 비식별 실제 화면, 읽기 전용 권한의 GitHub Actions가 기존에 공개되었다.
현재 변경의 hosted CI 상태는 README의 실제 workflow 링크와 해당 PR을 기준으로 한다.
별도 release tag는 생성하지 않았다.
