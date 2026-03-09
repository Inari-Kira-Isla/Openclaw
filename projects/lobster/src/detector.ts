// Detector Module - 自動偵測錯誤
import { exec } from 'child_process';
import { promisify } from 'util';
import { LobsterError, ErrorSource, ErrorSeverity } from './types';

const execAsync = promisify(exec);

export interface DetectionResult {
  source: ErrorSource;
  title: string;
  description: string;
  severity: ErrorSeverity;
  tags: string[];
  rawData?: unknown;
}

export class Detector {
  // 偵測 Cron Job 錯誤
  async detectCronErrors(): Promise<DetectionResult[]> {
    const results: DetectionResult[] = [];

    try {
      // 讀取 OpenClaw cron 狀態
      const { stdout } = await execAsync('openclaw status --json 2>/dev/null || echo "{}"');
      const status = JSON.parse(stdout);

      if (status.crons) {
        for (const cron of status.crons) {
          if (cron.status === 'error') {
            results.push({
              source: 'cron',
              title: `Cron Error: ${cron.name || cron.id}`,
              description: `Error message: ${cron.error || 'Unknown error'}`,
              severity: this.estimateSeverity(cron.error),
              tags: ['cron', 'automation', 'openclaw'],
              rawData: cron
            });
          }
        }
      }
    } catch (error) {
      console.log('Could not read cron status:', error);
    }

    return results;
  }

  // 偵測 API 錯誤
  async detectApiErrors(): Promise<DetectionResult[]> {
    // 這個需要結合 OpenClaw 的 API logs
    // 暫時返回空數組，後續可以擴展
    return [];
  }

  // 偵測 Session 錯誤（分析最近的失敗對話）
  async detectSessionErrors(): Promise<DetectionResult[]> {
    const results: DetectionResult[] = [];

    try {
      // 讀取最近的 session logs
      const { stdout } = await execAsync('ls -lt ~/.openclaw/logs/*.log 2>/dev/null | head -5');
      const logFiles = stdout.trim().split('\n');

      for (const logFile of logFiles) {
        const filePath = logFile.split(/\s+/).pop();
        if (!filePath) continue;

        try {
          const { stdout: logContent } = await execAsync(`tail -100 "${filePath}" 2>/dev/null`);
          
          // 檢測錯誤關鍵字
          const errorPatterns = [
            /error:?\s*(.+)/gi,
            /failed:?\s*(.+)/gi,
            /exception:?\s*(.+)/gi
          ];

          for (const pattern of errorPatterns) {
            let match;
            while ((match = pattern.exec(logContent)) !== null) {
              results.push({
                source: 'session',
                title: `Session Error Detected`,
                description: match[1] || 'Unknown error in session',
                severity: 'medium',
                tags: ['session', 'openclaw'],
                rawData: { file: filePath, line: match[0] }
              });
            }
          }
        } catch {
          // Skip unreadable files
        }
      }
    } catch {
      // No logs found
    }

    return results;
  }

  // 自動偵測所有來源
  async detectAll(): Promise<DetectionResult[]> {
    const [cronErrors, apiErrors, sessionErrors] = await Promise.all([
      this.detectCronErrors(),
      this.detectApiErrors(),
      this.detectSessionErrors()
    ]);

    return [...cronErrors, ...apiErrors, ...sessionErrors];
  }

  // 根據錯誤訊息估計嚴重程度
  private estimateSeverity(errorMsg?: string): ErrorSeverity {
    if (!errorMsg) return 'medium';
    
    const msg = errorMsg.toLowerCase();
    if (msg.includes('fatal') || msg.includes('critical') || msg.includes('crash')) {
      return 'high';
    } else if (msg.includes('warn') || msg.includes('timeout')) {
      return 'low';
    }
    return 'medium';
  }
}

export default Detector;
