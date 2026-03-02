export interface BoundingBox {
  x_min: number;
  y_min: number;
  x_max: number;
  y_max: number;
  confidence?: number;
  class_id?: number;
  class_name?: string;
}

