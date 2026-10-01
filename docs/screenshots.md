# Reporting Evidence Gallery

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

## Public execution document

아래는 관리자 서비스가 아닌 **공개 예제의 실제 실행 결과 문서**를 Chrome으로 캡처한 것입니다.
[JSON](../examples/execution.json) → [HTML](../examples/execution.html)을
[renderer](../src/render_evidence.py)가 생성하며 회귀 테스트가 저장본과 재실행을 비교합니다.

- [입력 계약](screenshots/inputs.png): origin·단위·기간을 유지하는 합성 관측.
- [분석](screenshots/analysis.png): 실제 Decimal 비교와 이력 부족 상태.
- [생성 보고서](screenshots/report.png): template 출력이며 LLM 결과가 아님.

[캡처 hash](screenshots/manifest.json)는 두 종류의 공개 파일을 식별합니다.
운영 캡처와 합성 결과를 같은 실행이나 같은 성과로 연결하지 않습니다.
