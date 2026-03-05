# GitHub 監控記錄

## 2026-03-04 09:35

### OpenClaw Repo

**PRs (10 items)**
| # | Title | Author | Status |
|---|-------|--------|--------|
| 33737 | Plugin SDK: add channel subpaths and migrate bundled plugins | codex | OPEN |
| 33735 | Add Chinese LLM providers: Deepseek, Zhipu (GLM), DashScope | Louis830903 | OPEN |
| 33733 | Align ingress, atomic paths with credential semantics | joshavant | OPEN |
| 33732 | fix(daemon): handle systemctl is-enabled exit code 4 | Clawborn | OPEN |
| 33727 | feat: per-agent thinkingDefault config | dgarson | OPEN |
| 33726 | fix(agents): always register Ollama provider when explicitly configured | dalefrieswthat | OPEN |

**Issues (5 bugs)**
| # | Title | Labels |
|---|-------|--------|
| 33730 | [Bug]: 为啥会这样啊 | bug, bug:behavior |
| 33698 | [Bug]: Ollama provider never initializes at runtime (2026.3.2) | bug, regression |
| 33685 | Bug Report: setup-podman.sh fails on Fedora Silverblue | bug, regression |
| 33650 | Chrome/Brave extension relay fails to attach | bug, regression |
| 33637 | Bug: Moonshot CN API doesn't work: HTTP 401 | bug, bug:behavior |

### 系統相關性判斷
- **Ollama provider bug (#33698)**: 可能相關，待觀察
- **Chinese LLM providers (#33735)**: 未來可能支援 Deepseek/Zhipu
- **per-agent thinkingDefault (#33727)**: 新功能，可研究

### 結論
✅ 無需立即討論，列入追蹤觀察
