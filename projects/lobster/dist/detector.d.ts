import { ErrorSource, ErrorSeverity } from './types';
export interface DetectionResult {
    source: ErrorSource;
    title: string;
    description: string;
    severity: ErrorSeverity;
    tags: string[];
    rawData?: unknown;
}
export declare class Detector {
    detectCronErrors(): Promise<DetectionResult[]>;
    detectApiErrors(): Promise<DetectionResult[]>;
    detectSessionErrors(): Promise<DetectionResult[]>;
    detectAll(): Promise<DetectionResult[]>;
    private estimateSeverity;
}
export default Detector;
