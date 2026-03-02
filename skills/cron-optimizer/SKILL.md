# Cron Optimizer Skill

**Purpose:** Analyze and optimize OpenClaw cron jobs for efficiency.

## Usage

When user asks to optimize cron/heartbeat, analyze and provide recommendations.

## Analysis Commands

```bash
# Get cron count
openclaw cron list | grep -c "cron\|every"

# Get frequency distribution
openclaw cron list | grep -oE 'cron \*/[0-9]+|every [0-9]+[mh]' | sort | uniq -c | sort -rn

# Find idle jobs
openclaw cron list | grep idle

# Find skipped jobs (not running)
openclaw cron list | grep skipped
```

## Consolidation Strategy

### High Frequency (*/5-*/15)
- Keep critical: auto-routing, vector sync
- Merge others → */15

### Medium Frequency (*/17-*/30)
- Merge → */30

### Low Frequency (hourly+)
- Already optimized

### Idle/Skipped Jobs
- Delete idle immediately
- Investigate skipped jobs

## Cleanup Commands

```bash
# Delete specific cron by ID
openclaw cron delete <job-id>

# Or use cron remove pattern (if available)
```

## Post-Optimization Monitoring

After consolidation, monitor:
1. Task success rate
2. Execution latency
3. Queue depth

---
Created: 2026-03-02
