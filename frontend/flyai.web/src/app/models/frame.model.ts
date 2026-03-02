import { DetectModel } from './detect.model';

export interface FrameModel {
  id: number;
  image_path: string;
  // name: string; ist nocht nicht implementiert
  // description: string; ist nocht nicht implementiert
  created_at: Date;
  video_id: number;
  track_id: number;
  detects: DetectModel[];
}
