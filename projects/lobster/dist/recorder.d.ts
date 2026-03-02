import { NotionClient } from './notion';
import { LobsterError, SuccessRecord, DetectionResult } from './types';
export declare class Recorder {
    private notion;
    constructor(notion: NotionClient);
    recordError(error: Omit<LobsterError, 'id' | 'createdAt' | 'updatedAt'>): Promise<string>;
    recordFromDetection(detection: DetectionResult): Promise<string>;
    recordSuccess(success: Omit<SuccessRecord, 'id' | 'createdAt'>): Promise<string>;
    resolveError(errorId: string, solution: string, prevention: string): Promise<void>;
    getOpenErrors(): Promise<void>;
    getStats(): Promise<void>;
}
export default Recorder;
