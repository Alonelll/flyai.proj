export interface OrientedBoundingBox {
  x_center: number;
  y_center: number;
  width: number;
  height: number;
  rotation: number;
  confidence?: number;
  class_id?: number;
  class_name?: string;
}

