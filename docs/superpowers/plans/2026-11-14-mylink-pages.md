# MyLink GitHub Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `ttuurrnn/mylink-folder`의 `MyLink/` 정적 페이지를 GitHub Pages에 배포하고 실제 접속을 검증한다.

**Architecture:** 의존성 없는 HTML/CSS 파일을 `MyLink/`에 둔다. GitHub Actions는 이 디렉터리만 Pages artifact로 업로드하여 저장소의 project-site 루트 URL에 배포한다.

**Tech Stack:** HTML5, CSS3, Python 3 `unittest`, GitHub Actions, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-11-14-mylink-pages-design.md`

## Global Constraints

- 공개 저장소 이름은 정확히 `mylink-folder`이다.
- 사이트 소스는 정확히 `MyLink/` 아래에 둔다.
- 외부 패키지, 사용자 입력, 방문자 추적을 사용하지 않는다.
- 확인된 공개 URL만 링크한다.
- 예상 공개 URL은 `https://ttuurrnn.github.io/mylink-folder/`이다.

## Review Focus

- 저장소 이름의 대소문자와 Pages project-site URL이 일치해야 한다. Task 3의 live URL 검사로 고정한다.
- Actions artifact에 `MyLink/` 폴더 자체가 한 단계 더 포함되지 않아야 한다. Task 3의 실제 Pages URL 루트 검사로 고정한다.
- 모든 상대 정적 리소스가 `MyLink/` 안에서 해석되어야 한다. Task 1의 링크 대상 존재 검사로 고정한다.
- 외부 링크는 HTTPS이며 새 탭 사용 시 `rel="noopener noreferrer"`가 있어야 한다. Task 1의 HTML 검사로 고정한다.
- Pages 배포 권한과 environment 설정이 누락되지 않아야 한다. Task 3의 실제 workflow 성공 상태 검사로 고정한다.

---

### Task 0: 로컬 저장소 초기화와 설계 기록

**Files:**
- Include: `docs/superpowers/specs/2026-11-14-mylink-pages-design.md`
- Include: `docs/superpowers/plans/2026-11-14-mylink-pages.md`

**Interfaces:**
- Consumes: 승인된 설계와 구현 계획
- Produces: `main` 브랜치의 로컬 Git 저장소와 재현 가능한 설계 기록

- [ ] **Step 1: 로컬 Git 저장소를 초기화한다**

  Run: `git init -b main`
  Expected: current branch is `main`.

- [ ] **Step 2: 설계 및 계획 문서를 첫 커밋으로 기록한다**

  `git add docs && git commit -m "docs: plan MyLink GitHub Pages site"`

- [ ] **Step 3: 작업 트리가 깨끗한지 확인한다**

  Run: `git status --short --branch`
  Expected: `## main` with no changed paths.

### Task 1: 정적 MyLink 페이지

**Files:**
- Create: `tests/test_mylink.py`
- Create: `MyLink/index.html`
- Create: `MyLink/styles.css`
- Create: `MyLink/.nojekyll`

**Interfaces:**
- Consumes: 공개 GitHub URL `https://github.com/ttuurrnn`
- Produces: `MyLink/index.html`을 진입점으로 하는 독립 정적 사이트 디렉터리

- [ ] **Step 1: 실패하는 정적 사이트 검사를 작성한다**

  `test_required_files_exist`, `test_html_identity_and_https_links`, `test_local_assets_exist`, `test_external_blank_links_are_hardened`가 위 파일과 문구, 링크 보안 속성을 검증한다.

- [ ] **Step 2: 검사가 실패함을 확인한다**

  Run: `python -m unittest tests.test_mylink -v`
  Expected: FAIL because `MyLink/index.html` does not exist.

- [ ] **Step 3: 최소 HTML/CSS 페이지를 구현한다**

  `index.html`은 `MyLink` 제목, 짧은 안내 문구, GitHub 프로필 링크를 제공한다. `styles.css`는 키보드 focus 상태, 작은 화면 대응, `prefers-reduced-motion`을 포함한다.

- [ ] **Step 4: 정적 사이트 검사를 통과시킨다**

  Run: `python -m unittest tests.test_mylink -v`
  Expected: 4 tests, OK.

- [ ] **Step 5: Task 1을 커밋한다**

  `git add MyLink tests/test_mylink.py && git commit -m "feat: add MyLink static page"`

### Task 2: GitHub Pages workflow

**Files:**
- Create: `tests/test_verify_site.py`
- Create: `scripts/verify_site.py`
- Create: `.github/workflows/pages.yml`

**Interfaces:**
- Consumes: Task 1의 `MyLink/` 사이트 디렉터리
- Produces: 정적 사이트 검증 CLI와 `MyLink/`의 내용을 Pages site root로 배포하는 workflow

- [ ] **Step 1: 실패하는 정적 사이트 검증기 테스트를 작성한다**

  `test_valid_site_has_no_errors`, `test_missing_local_asset_is_reported`, `test_insecure_external_link_is_reported`가 실제 임시 사이트 트리를 사용해 검증 결과를 확인한다.

- [ ] **Step 2: 검증기 테스트가 실패함을 확인한다**

  Run: `python -m unittest tests.test_verify_site -v`
  Expected: FAIL because `scripts.verify_site` does not exist.

- [ ] **Step 3: 최소 정적 사이트 검증기를 구현한다**

  `verify_site(site_dir: Path) -> list[str]`는 `index.html`을 파싱해 존재하지 않는 상대 파일과 안전하지 않은 외부 링크를 오류로 반환한다. CLI는 오류가 있으면 비정상 종료한다.

- [ ] **Step 4: 검증기 테스트를 통과시킨다**

  Run: `python -m unittest tests.test_verify_site -v`
  Expected: 3 tests, OK.

- [ ] **Step 5: Pages workflow를 구현하고 로컬 사이트 검증을 실행한다**

  `main` push와 수동 실행을 지원한다. build job은 `python scripts/verify_site.py MyLink`를 실행하고 `./MyLink`를 정적 artifact로 업로드한다. deploy job은 `pages: write`, `id-token: write`, `environment: github-pages`, `actions/deploy-pages`를 사용한다.

- [ ] **Step 6: 전체 로컬 검사를 통과시킨다**

  Run: `python -m unittest discover -s tests -v`
  Expected: 7 tests, OK.

- [ ] **Step 7: Task 2를 커밋한다**

  `git add .github/workflows/pages.yml scripts/verify_site.py tests/test_verify_site.py && git commit -m "ci: verify and deploy MyLink with GitHub Pages"`

### Task 3: 저장소 생성, 배포, 실접속 검증

**Files:**
- Publish: all committed repository files

**Interfaces:**
- Consumes: Task 1 정적 사이트와 Task 2 workflow
- Produces: 공개 GitHub 저장소 URL과 실제 GitHub Pages URL

- [ ] **Step 1: 공개 `ttuurrnn/mylink-folder` 저장소를 생성한다**

  Expected: default branch `main`, visibility `public`.

- [ ] **Step 2: 로컬 커밋을 원격 `main`에 게시한다**

  Expected: GitHub에서 `MyLink/`, `.github/workflows/pages.yml`, `docs/`, `tests/`를 확인할 수 있다.

- [ ] **Step 3: Pages source가 GitHub Actions인지 확인한다**

  Expected: Pages deployment workflow가 `verify`, `upload`, `deploy` 단계를 거쳐 성공한다.

- [ ] **Step 4: 실제 URL을 검증한다**

  Run: `Invoke-WebRequest -Uri 'https://ttuurrnn.github.io/mylink-folder/' -UseBasicParsing`
  Expected: HTTP 200, final URL remains the project-site root, and response body contains `<title>MyLink</title>`.

- [ ] **Step 5: 제출 정보를 확정한다**

  저장소 URL과 MyLink URL을 과제 양식 두 줄로 제공하고, GitHub UI에서 재확인할 위치를 함께 안내한다.
