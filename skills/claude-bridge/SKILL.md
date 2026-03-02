---
name: claude-bridge
description: Route requests to Claude Code via the ACP bridge. Use when user invokes /claude command.
user-invocable: true
trigger:
  command: /claude
---

# Claude Bridge Skill

When the user invokes `/claude <task>`, route the task to Claude Code via ACP.

## Behavior

1. Extract the task text after `/claude`.
2. Use `sessions_spawn` with:
   - `runtime: "acp"`
   - `agentId: "claude"`
   - `thread: true`
   - `mode: "session"`
   - `task: <extracted task text>`
3. Stream results back to the user in the same chat.
4. If the task involves code execution, file operations, or web search, Claude Code will handle them with its full tool suite.

## Examples

- `/claude analyze the memory files in ~/.openclaw/memory/`
- `/claude review the code in ~/openclaw-brain`
- `/claude write a Python script to backup Notion databases`
- `/claude search the web for latest AI agent frameworks`
- `/claude check system status and summarize`
