### hi 👋

builder & tinkerer — AI agents, prediction markets, pet apps

---

## 🏗️ Build Studio — AI 에이전트 프로덕트 빌딩 시스템

18명의 AI 에이전트가 자율 협업하여 앱을 기획→설계→개발→검증→출시하는 시스템.

### 에이전트 구성

| 역할 | 에이전트 | 모델 | 하는 일 |
|---|---|---|---|
| **전략** | CEO | Claude Opus 4.6 | 최종 판단, 출시 승인, 4대 지표 평가 |
| **기술** | CTO | Claude Opus 4.6 | 작업 분해→개발자 할당, 코드 리뷰(10점) |
| **기획** | CPO | Gemini 2.5 Pro | UX/UI 설계, PRD, 사용성 테스트 |
| **그로스** | Viral | Gemini 2.5 Pro | 바이럴 K-factor 검증, 네트워크 효과 |
| **설계** | Blueprint | Gemini 2.5 Pro | 아키텍처, DB/API 설계 |
| **QA** | Shield | Gemini 2.5 Pro | 보안 감사, TDD, 의료 가드레일 |
| **개발** | FE/BE/FS Dev | Codex GPT-5.3 | Flutter/Supabase 코드 작성 |
| **리서치** | 8명 | Gemini 2.5 Pro | 예측마켓 분석, 시장 리서치 |

### 사용 시스템

| 시스템 | 용도 |
|---|---|
| [Paperclip](https://paperclip.ing) | 에이전트 오케스트레이션 (로컬) |
| Claude Code (Opus 4.6) | 사령관 인터페이스 + Paperclip 관리 |
| Gemini CLI (2.5 Pro) | 기획/검증/리서치 (비용 $0) |
| Codex (GPT-5.3) | 코드 작성 엔진 |
| Telegram Bot | 모바일 지시/보고 |

### 작업 공정 (Infinity Harness v1.0)

```
Step 0: 보드진 → CEO 지시
Step 1: CEO + CPO → 가설 정의
Step 2: Viral → 가설 검증 (게이트키퍼) ← 통과 전 설계/개발 금지
Step 3: CPO/Blueprint/Shield → 병렬 설계
Step 4: CTO → 작업 분해 + 개발자 할당
Step 5: Codex 개발자 → 구현
Step 6: CTO→Viral→Shield 3단 검증 (7점 미만 재작업)
Step 7: CEO 종합 평가 (80점 기준)
```

### Claude ↔ Gemini 공유 메모리

Claude 토큰 소진 시 Gemini가 즉시 이어받는 구조.

```
~/.shared-memory/
├── short-term/today.md     ← 매 세션 자동 로드 (오늘 맥락)
├── long-term/              ← 필요할 때만 검색 (영구 정보)
│   ├── agents.md           에이전트 ID/설정
│   ├── projects.md         프로젝트 정보
│   ├── decisions.md        보드진 결정 기록
│   └── bugs.md             알려진 버그/패치
├── handoff/active.md       ← 세션 교체 시 인수인계
└── archive.sh              ← 자정 자동 아카이빙
```

**단기 기억**: `today.md` — 매 세션 자동 로드, 자정에 장기로 아카이빙
**장기 기억**: `long-term/*.md` — 매번 안 읽고 필요할 때 grep
**인수인계**: `handoff/active.md` — "지금 당장 해야 할 일"

| 상황 | 동작 |
|---|---|
| Claude 시작 | today.md + active.md 자동 로드 |
| Gemini 시작 | 동일 (GEMINI.md에서 참조) |
| Claude 토큰 소진 | today.md에 기록 남아있음 → Gemini 이어받음 |
| 자정 | today.md → long-term/daily/날짜.md 아카이빙 |

### 자동화

- **auto-resume**: 5분마다 error 에이전트 자동 복구 (Gemini/Codex만, Claude 제외)
- **자정 아카이빙**: 단기→장기 자동 이동
- **텔레그램 봇**: `/bs` 커맨드로 모바일에서 지시

---

[![GitHub](https://img.shields.io/badge/-bugbug9999-181717?style=flat&logo=github)](https://github.com/bugbug9999)
