import { NotionClient } from './notion';
import { Prevention, NotionPage } from './types';
export declare class ReviewEngine {
    private notion;
    constructor(notion: NotionClient);
    checkBeforeAction(action: string, context?: string): Promise<Prevention[]>;
    getDailyReview(): Promise<{
        openErrors: number;
        highSeverity: number;
        recentErrors: NotionPage[];
        trend: 'improving' | 'stable' | 'worsening';
    }>;
    getWeeklySummary(): Promise<string>;
    private extractKeywords;
}
export default ReviewEngine;
