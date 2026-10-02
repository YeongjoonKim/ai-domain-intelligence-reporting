# Security — Data Provenance & Human Validation

생성 HTML과 입력 데이터는 외부에 그대로 신뢰하지 않는다. 공개 예제는 합성 입력만 사용하며 운영 수신자·메일 주소·DB 접속 문자열은 저장하지 않는다. 자동 검증과 사람 승인은 서로 다른 상태다.

## Reporting

GitHub private vulnerability reporting이 활성화된 경우 해당 채널을 사용한다.
비활성화된 경우 민감정보 없이 비공개 연락 채널을 요청한다. 공개 issue에 secret이나
개인 데이터를 첨부하지 않는다. 응답 기한이나 운영 서비스 보안 보증은 제공하지 않는다.

## Checks and limits

`python3 scripts/check_repository.py`는 구문·JSON·로컬 링크·PNG 구조/manifest와
도달 가능한 Git history의 제한된 secret 패턴을 검사한다. semantic/IP 검토, 이미지 내 개인정보,
외부 링크 안전성이나 secret 부재를 증명하는 전문 감사 도구는 아니다.
CI는 고정 action revision, contents read 권한을 사용하고 repository secret을 요구하지 않는다.
GitHub 보안 기능의 활성 상태는 별도로 확인해야 하며 이 문서는 설정 변경을 주장하지 않는다.
