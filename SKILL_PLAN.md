# Muse-Core 技能建設計畫

## 總覽
- **目標**: 建立 12 個 Agent 所需的所有自訂技能
- **位置**: `/Users/ki/.openclaw/workspace/skills/`

## 技能清單

### Phase 1: 核心層 (Core Layer)

#### muse-core (4 skills)
| Skill | 功能 |
|-------|------|
| workflow_router | 任務分發到正確的 Agent |
| gscc_classifier | GSCC 風險分級判定 |
| final_verdict | 最終裁決與結果整合 |
| result_integrator | 整合多 Agent 結果 |

#### workflow-orchestrator (3 skills)
| Skill | 功能 |
|-------|------|
| workflow_execution | 執行多步驟工作流 |
| state_control | 狀態管理與追蹤 |
| task_scheduling | 任務排程與優先級 |

---

### Phase 2: 建構層 (Builder Layer)

#### mcp-builder (2 skills)
| Skill | 功能 |
|-------|------|
| scaffold_server | MCP Server 骨架生成 |
| fault_tolerance | 容錯與錯誤處理 |

#### skill-creator (2 skills)
| Skill | 功能 |
|-------|------|
| expert_skill_md | 專家級 SKILL.md 撰寫 |
| skill_generator | 自動化技能生成 |

#### verification-agent (3 skills)
| Skill | 功能 |
|-------|------|
| scenario_simulation | 情境模擬測試 |
| failure_analysis | 失敗分析與報告 |
| config_validation | 配置驗證 |

---

### Phase 3: 記憶層 (Memory Layer)

#### memory-agent (4 skills)
| Skill | 功能 |
|-------|------|
| semantic_ingest | 語義資料攝入 |
| conflict_detection | 衝突檢測 |
| decay_monitor | 記憶衰減監控 |
| memory_organization | 記憶整理與分類 |

---

### Phase 4: 進化層 (Evolution Layer)

#### skill-slime-agent (4 skills)
| Skill | 功能 |
|-------|------|
| skill_ingestion | 技能攝入與學習 |
| fusion_proposal | 技能融合建議 |
| version_tracking | 版本追蹤 |
| skill_evolution | 技能演進管理 |

#### self-evolve-agent (4 skills)
| Skill | 功能 |
|-------|------|
| drift_detection | 漂移檢測 |
| prompt_refinement | Prompt 優化 |
| workflow_improvement | 工作流改進 |
| performance_analysis | 效能分析 |

#### agent-builder (4 skills)
| Skill | 功能 |
|-------|------|
| requirement_analyzer | 需求分析 |
| architecture_designer | 架構設計 |
| config_generator | 配置生成 |
| auto_builder | 自動化建構 |

---

### Phase 5: 防護層 (Security Layer)

#### security-agent (5 skills)
| Skill | 功能 |
|-------|------|
| api_key_audit | API 金鑰審計 |
| access_log_monitor | 存取日誌監控 |
| vulnerability_scanner | 漏洞掃描 |
| anomaly_detector | 異常檢測 |
| security_report | 安全報告生成 |

#### monitor-agent (5 skills)
| Skill | 功能 |
|-------|------|
| data_growth_monitor | 資料成長監控 |
| load_balancer | 負載平衡 |
| performance_optimizer | 效能優化 |
| archive_manager | 歸檔管理 |
| alert_manager | 警報管理 |

#### reminder-agent (5 skills)
| Skill | 功能 |
|-------|------|
| bni_meeting_reminder | BNI 會議提醒 |
| bni_weekly_report_reminder | 每週報告提醒 |
| followup_reminder | 跟進提醒 |
| daily_checkin_reminder | 每日簽到提醒 |
| monthly_review_reminder | 月度回顧提醒 |

---

### Phase 6: 業務層 (Business Layer)

#### bni-agent (4 skills)
| Skill | 功能 |
|-------|------|
| member_management | 會員管理 |
| referral_tracker | 轉介紹追蹤 |
| bni_recommender | 推薦系統 |
| analytics_report | 數據報告 |

#### facebook-agent (5 skills)
| Skill | 功能 |
|-------|------|
| facebook_messenger_handler | Messenger 處理 |
| question_classifier | 問題分類 |
| faq_auto_reply | FAQ 自動回覆 |
| handoff_manager | 轉接管理 |
| conversation_logger | 對話記錄 |

#### crm-agent (5 skills)
| Skill | 功能 |
|-------|------|
| contact_management | 聯絡人管理 |
| interaction_tracker | 互動追蹤 |
| value_scorer | 價值評分 |
| followup_reminder | 跟進提醒 |
| customer_analytics | 客戶分析 |

#### analytics-agent (4 skills)
| Skill | 功能 |
|-------|------|
| referral_analytics | 轉介紹分析 |
| question_analytics | 問題分析 |
| performance_report | 效能報告 |
| trend_analysis | 趨勢分析 |

#### knowledge-agent (4 skills)
| Skill | 功能 |
|-------|------|
| faq_management | FAQ 管理 |
| qa_learning | Q&A 學習 |
| template_updater | 範本更新 |
| knowledge_search | 知識搜尋 |

---

### Phase 7: 治理層 (Governance Layer)

#### governance-agent (3 skills)
| Skill | 功能 |
|-------|------|
| risk_assessment | 風險評估 |
| rule_enforcement | 規則執行 |
| conflict_resolution | 衝突解決 |

---

### Phase 8: 生活 OS 層

#### lifeos-agent (4 skills)
| Skill | 功能 |
|-------|------|
| daily_scan | 每日掃描 |
| expense_logging | 支出記錄 |
| schedule_management | 日程管理 |
| information_gathering | 資訊收集 |

---

## 總計
- **8 個 Agent 群組**
- **63 個自訂技能**
- **預估時間**: 分批建立

## 建構順序
1. 先建立核心技能 (muse-core + workflow-orchestrator)
2. 再建構建構類技能
3. 最後建業務類技能
