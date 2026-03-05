/**
 * Represents a detected bounding box (DetectedBoxResponse from Python API)
 */
export interface DetectedBox {
  id: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  confidence: number;
  class_id: number;
  class_name?: string;
  tracking_id?: number;
}

