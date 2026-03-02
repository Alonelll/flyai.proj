export interface DetectModel {
  id: number;
  frame_id: number;
  label: string;
  confidence: number;
  bbox_x: number;
  bbox_y: number;
  bbox_width: number;
  bbox_height: number;
  // created_at: string; Ist nocht nicht implementiert
  // updated_at: string; Ist nocht nicht implementiert
}
