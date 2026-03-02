export type ErrorSeverity = 'high' | 'medium' | 'low';
export type ErrorSource = 'cron' | 'api' | 'session' | 'manual';
export type RecordStatus = 'open' | 'resolved' | 'monitoring';
export interface LobsterError {
    id?: string;
    source: ErrorSource;
    severity: ErrorSeverity;
    title: string;
    description: string;
    cause?: string;
    solution?: string;
    prevention?: string;
    tags: string[];
    status: RecordStatus;
    occurrenceCount: number;
    createdAt: Date;
    updatedAt: Date;
}
export interface SuccessRecord {
    id?: string;
    title: string;
    workflow: string;
    description: string;
    tags: string[];
    lessons: string[];
    createdAt: Date;
}
export interface Prevention {
    errorId: string;
    title: string;
    prevention: string;
    severity: ErrorSeverity;
}
export interface LobsterConfig {
    notionApiKey: string;
    databaseId: string;
    successDatabaseId: string;
}
export interface NotionPage {
    id: string;
    created_time: string;
    last_edited_time: string;
    properties: Record<string, unknown>;
}
export interface DetectionResult {
    source: ErrorSource;
    title: string;
    description: string;
    severity: ErrorSeverity;
    tags: string[];
    rawData?: unknown;
}
