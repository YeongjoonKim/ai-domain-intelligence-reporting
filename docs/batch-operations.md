# Source collection and batch operations

수집은 리포트 함수 호출 이전의 별도 실행 단계입니다. 관리자에서 소스 상태와 저장된 배치 실행,
각 단계의 종료 상태를 확인하고 허용된 전체 실행 또는 실패 단계 재시도를 요청할 수 있습니다.

`Admin action → authenticated API → signed request → host runner → per-stage result`

API는 허용된 파이프라인·단계와 관리자 권한을 검사합니다. 호스트 실행기는 서명을 검증하고
등록된 배치만 시작하며, 관리 화면에서 실행 중 여부와 단계별 시간·오류를 확인합니다.
[서비스·배치 제어의 공통 경계](https://github.com/YeongjoonKim/reliable-domain-agent-harness/blob/main/docs/execution-control.md)를 재사용합니다.

![저장된 배치 이력과 단계별 상태](screenshots/batch-execution.png)

2026-10-03 현재 UI에서 기존 실행 기록을 조회한 화면입니다. 부분 실패와 `확인 불가` 표시를 유지했습니다.
상위 실행의 성공과 모든 하위 단계의 관측 완료는 다른 의미입니다. 수집 실행 완료를 원천 데이터 전체의
적재·최신성 보증으로 해석하지 않습니다.

촬영에서는 저장된 실행 이력 조회 helper와 읽기 전용 DB 트랜잭션을 사용했습니다.
원래 상태 조회 API에 있는 과거 로그 동기화·상태 갱신은 실행하지 않았습니다.
새 수집·재시도·재색인·리포트 생성·발송도 수행하지 않았습니다.

## From execution to report evidence

| 단계 | 관리하는 것 | 리포트와의 연결 |
|---|---|---|
| 배치 실행 | 실행 ID, 단계, 시간, 결과 | 어떤 수집이 완료·실패했는지 관측 |
| 원천 저장 | 문서 버전·공식 행·기간·단위 | 분석 대상과 원문 출처 유지 |
| 검수·선택 | 보고서·지표 상태와 승인 텍스트 | 적격 정형 자료와 정성 입력 구분 |
| 생성·검토 | 계산, 근거 설명, 품질·승인 | 사업 영역별 보고서 산출 |

[현재 아키텍처](architecture/01_reporting_architecture.svg) · [데이터에서 리포트까지](data-to-report.md).
