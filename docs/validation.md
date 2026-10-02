# Validation / 검증 기록

## Data-to-Report Expansion · 2026-10-02

- 40개 데이터 테이블의 읽기 전용 집계와 기존 보고서 조회 함수의 선택 결과를 대조.
- 현재 DB의 예보·적산온도 섹션과 과거 저장본의 인사이트 상단 등 3개 화면 추가.
- 공개 테스트 **25개 통과**, 저장소 검사와 diff 공백 검사 통과.
- 기존 private reporting 회귀는 **243개 통과·2개 실패**. 공개 테스트나 모델 성능과 구분.
- KREI 현재 버전 검수 gate의 정형 입력 0건, 한글화 제목과 품질 검사 간 계약 불일치를 후속 과제로 기록.
- 원본 화면을 보존하고 공개 사본의 식별 정보·metadata·hash를 검토. 운영 생성·발송·승인 상태 변경 없음.

[상세 관측](data-to-report.md)과 [화면 출처](screenshots.md)를 함께 확인합니다.

## Actual Engineering Review · 2026-10-02

공개 예제 검증과 별도로 실제 구현·설정·읽기 전용 API·관리자 화면을 재검토했습니다.
[실제 근거](actual-engineering.md)와 [화면 갤러리](screenshots.md)에 관측 범위를 기록합니다.
운영 데이터·학습·모델 적용·발송·정책 승인은 변경하지 않았습니다.

## Public Sample Validation · 2026-10-01

2026-10-01. 공개 재구성 예제만 검증했으며 운영 API·DB·GPU를 사용하지 않았습니다.

- 로컬 Python 3.10.12: **22개 테스트 통과**.
- 기본 CLI와 execution exporter 실행 성공.
- 저장된 실행 artifact와 재계산 결과를 회귀 테스트로 비교.
- 공개 실행 snapshot을 Chrome으로 캡처하고, 별도 승인된 운영 UI 크롭/마스킹 사본을 시각 검토.
- 무편집 원본은 비공개로 보존. 공개 사본은 픽셀 평탄화·metadata 제외·SHA-256 manifest 검사.
- 상대 문서 링크, Python 구문, JSON, 제한된 secret pattern과 Git history 검사.
- PNG는 검토한 hash와 구조/metadata를 검사. 이미지 속 개인정보 부재는 자동 보증하지 않음.
- 첫 공개 main의 GitHub CI(Python 3.10/3.12)는 성공 상태를 확인함.
- 보완본의 정확한 CI 상태는 [Actions](https://github.com/YeongjoonKim/ai-domain-intelligence-reporting/actions/workflows/ci.yml)에서 commit별로 확인.


코드 계약 검증, 모델 품질 평가, 공개 권리 검토는 각각 별도로 수행합니다.
공개 승인은 받았으며 별도의 오픈소스 라이선스는 아직 선택하지 않았습니다.
