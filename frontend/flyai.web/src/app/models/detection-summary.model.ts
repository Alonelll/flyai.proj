/**
 * Summary of all detections (DetectionSummary from Python API)
 */
export interface DetectionSummary {
  total_results: number;
  total_detections: number;
  average_confidence: number;
  unique_classes: string[];
}

