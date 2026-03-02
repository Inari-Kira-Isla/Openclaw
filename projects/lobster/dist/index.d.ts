import { LobsterConfig, LobsterError, SuccessRecord } from './types';
export declare class Lobster {
    private notion;
    private detector;
    private recorder;
    private review;
    constructor(config: LobsterConfig);
    autoDetectAndRecord(): Promise<number>;
    addError(error: Omit<LobsterError, 'id' | 'createdAt' | 'updatedAt'>): Promise<string>;
    addSuccess(success: Omit<SuccessRecord, 'id' | 'createdAt'>): Promise<string>;
    checkBeforeAction(action: string, context?: string): Promise<import("./types").Prevention[]>;
    getDailyReview(): Promise<{
        openErrors: number;
        highSeverity: number;
        recentErrors: import("./types").NotionPage[];
        trend: "improving" | "stable" | "worsening";
    }>;
    getWeeklySummary(): Promise<string>;
    getStats(): Promise<void>;
}
export default Lobster;
