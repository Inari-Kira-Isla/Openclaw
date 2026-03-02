import { LobsterError, SuccessRecord, LobsterConfig, NotionPage } from './types';
export declare class NotionClient {
    private client;
    private config;
    constructor(config: LobsterConfig);
    createErrorRecord(error: Omit<LobsterError, 'id' | 'createdAt' | 'updatedAt'>): Promise<string>;
    createSuccessRecord(success: Omit<SuccessRecord, 'id' | 'createdAt'>): Promise<string>;
    searchErrors(keyword: string): Promise<NotionPage[]>;
    getOpenErrors(): Promise<NotionPage[]>;
    updateErrorStatus(pageId: string, status: string): Promise<void>;
    getErrorStats(): Promise<{
        total: number;
        open: number;
        resolved: number;
        bySeverity: Record<string, number>;
    }>;
}
