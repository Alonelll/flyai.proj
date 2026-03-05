import { DetectedBox } from './bounding-box.model';

/**
 * Represents a detection result with all associated boxes
 * Corresponds to ExpectedResultResponse from Python API
 */
export interface DetectionResult {
  id: number;
  source?: string;
  model_name?: string;
  created_at?: string;
  boxes: DetectedBox[];
}
