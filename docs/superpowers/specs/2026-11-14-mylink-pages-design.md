# MyLink GitHub Pages Design

## 의도

과제의 두 채점 조건을 명확하게 충족한다. GitHub 사용자 `ttuurrnn`의 공개 저장소에 `MyLink/` 전용 폴더를 두고, 누구나 실제 접속할 수 있는 GitHub Pages URL을 제공한다.

## 목표와 완료 조건

- 공개 저장소 이름은 `mylink-folder`로 한다.
- 저장소 안에 `MyLink/index.html`, `MyLink/styles.css`, `MyLink/.nojekyll`을 둔다.
- 페이지에는 `MyLink` 제목과 실제 공개된 `ttuurrnn` GitHub 링크만 사용한다.
- 모바일과 데스크톱에서 링크를 읽고 선택할 수 있어야 한다.
- GitHub Actions가 `MyLink/`의 내용만 Pages 사이트 루트로 배포한다.
- `https://ttuurrnn.github.io/mylink-folder/`가 HTTP 성공 응답을 반환하고 `MyLink` 문구를 포함해야 한다.

## 비목표와 제약

- 로그인, 데이터베이스, 방문자 추적, 사용자 입력, 외부 JavaScript 패키지는 추가하지 않는다.
- 확인되지 않은 개인 정보나 SNS 주소를 만들지 않는다.
- 기존 공개 저장소는 변경하지 않는다.
- 저장소와 Pages 사이트는 과제 제출을 위해 공개 상태여야 한다.

## 검토한 접근 방식

1. **새 공개 저장소 + `MyLink/` + Actions 배포 — 선택됨.** 기존 프로젝트와 분리되며 폴더 존재와 URL을 각각 명확하게 증명할 수 있다.
2. 기존 저장소 루트에서 Pages 배포. 설정은 단순하지만 기존 프로젝트 파일이 함께 공개되거나 배포 설정과 충돌할 수 있다.
3. 기존 저장소의 `/docs`를 Pages source로 사용. Actions가 필요 없을 수 있지만 과제에서 요구하는 `MyLink/` 전용 폴더와 공개 URL의 대응 관계가 덜 명확하다.

## 구조와 데이터 흐름

브라우저 요청 → GitHub Pages → Actions가 배포한 정적 artifact → `index.html` → `styles.css`. 사용자가 링크를 선택하면 GitHub의 공개 프로필로 이동한다. 서버 측 처리와 신뢰 경계 밖의 사용자 입력은 없다.

## 검증

로컬 자동 검사는 필수 파일, HTML 제목, HTTPS 링크, 로컬 정적 자산 참조를 실제 HTML 파싱으로 확인한다. workflow 설정은 소스 문자열 검사가 아니라 GitHub Actions 실행 결과로 검증하며, 배포 후 저장소 경로와 실제 URL의 HTTP 상태 및 본문을 별도로 확인한다.
