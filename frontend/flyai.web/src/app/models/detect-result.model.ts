import { BoundingBox } from './bounding-box.model';
import { ClassificationProb } from './classification-prob.model';
import { Keypoint } from './keypoint.model';
import { Mask } from './mask.model';
import { OrientedBoundingBox } from './oriented-bounding-box.model';

export interface DetectionResult {
  id: number;
  boxes: BoundingBox[] | null;
  masks: Mask[] | null;
  keypoints: Keypoint[] | null;
  probs: ClassificationProb[] | null;
  obb: OrientedBoundingBox[] | null;
}
