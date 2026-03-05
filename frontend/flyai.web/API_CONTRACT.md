# API Contract for Frontend

This document defines the API endpoints and response structures expected by the Angular frontend.

## Base URL
```
/api
```

---

## Endpoints

### 1. GET `/api/results`
**Purpose**: Fetch paginated detection results with lazy loading support

**Query Parameters** (Optional):
- `skip`: number (default: 0) - Records to skip
- `limit`: number (default: 10) - Records per page
- `sortField`: string - Field to sort by (e.g., "id", "created_at", "model_name")
- `sortOrder`: 1 | -1 - Sort direction (1 = ascending, -1 = descending)

**Response** (200 OK):
```json
{
  "results": [
    {
      "id": 1,
      "source": "camera_1",
      "model_name": "YOLOv8",
      "created_at": "2026-03-05T10:30:00Z",
      "boxes": [
        {
          "id": 101,
          "x1": 100.5,
          "y1": 150.2,
          "x2": 200.5,
          "y2": 250.2,
          "confidence": 0.95,
          "class_id": 1,
          "class_name": "person",
          "tracking_id": null
        },
        {
          "id": 102,
          "x1": 300.0,
          "y1": 50.0,
          "x2": 400.0,
          "y2": 200.0,
          "confidence": 0.87,
          "class_id": 2,
          "class_name": "car",
          "tracking_id": 5
        }
      ]
    },
    // ... more results
  ],
  "total": 150
}
```

**Error** (500):
```json
{
  "error": "Internal server error",
  "message": "Optional detailed error message"
}
```

---

### 2. GET `/api/result/{id}`
**Purpose**: Fetch a single detection result by ID

**Parameters**:
- `id`: number (path parameter) - Detection result ID

**Response** (200 OK):
```json
{
  "id": 1,
  "source": "camera_1",
  "model_name": "YOLOv8",
  "created_at": "2026-03-05T10:30:00Z",
  "boxes": [
    {
      "id": 101,
      "x1": 100.5,
      "y1": 150.2,
      "x2": 200.5,
      "y2": 250.2,
      "confidence": 0.95,
      "class_id": 1,
      "class_name": "person",
      "tracking_id": null
    }
  ]
}
```

**Error** (404):
```json
{
  "error": "Not found",
  "message": "Detection result with ID 1 not found"
}
```

---

### 3. GET `/api/summary`
**Purpose**: Fetch summary statistics for all detections

**Response** (200 OK):
```json
{
  "total_results": 150,
  "total_detections": 1250,
  "average_confidence": 0.87,
  "unique_classes": [
    "person",
    "car",
    "truck",
    "bicycle"
  ]
}
```

---

## Model Definitions

### DetectionResult
```typescript
interface DetectionResult {
  id: number;
  source?: string;
  model_name?: string;
  created_at?: string;  // ISO 8601 datetime
  boxes: DetectedBox[];
}
```

### DetectedBox
```typescript
interface DetectedBox {
  id: number;
  x1: number;        // Top-left X coordinate
  y1: number;        // Top-left Y coordinate
  x2: number;        // Bottom-right X coordinate
  y2: number;        // Bottom-right Y coordinate
  confidence: number; // 0.0 to 1.0
  class_id: number;   // Classification ID
  class_name?: string; // Human-readable class name
  tracking_id?: number; // Optional tracking identifier
}
```

### DetectionSummary
```typescript
interface DetectionSummary {
  total_results: number;
  total_detections: number;
  average_confidence: number;
  unique_classes: string[];
}
```

---

## Frontend Expectations

1. **Pagination**: Backend should support `skip` and `limit` parameters
2. **Sorting**: Backend should support `sortField` and `sortOrder` parameters
3. **Filtering**: Currently not implemented in frontend, but extensible
4. **Error Handling**: All errors should return proper HTTP status codes
5. **CORS**: If frontend and backend are on different domains, enable CORS
6. **Date Format**: Use ISO 8601 format for all datetime fields

---

## Example Requests

### Fetch first 10 results, sorted by creation date (newest first)
```
GET /api/results?skip=0&limit=10&sortField=created_at&sortOrder=-1
```

### Fetch next page (page 2 with 10 items per page)
```
GET /api/results?skip=10&limit=10
```

### Fetch with model sorting
```
GET /api/results?skip=0&limit=20&sortField=model_name&sortOrder=1
```

---

## Error Handling

The frontend expects standard HTTP error codes:

- **200 OK**: Request successful
- **404 Not Found**: Resource doesn't exist
- **500 Internal Server Error**: Server error
- **Other**: Any standard HTTP error code

All error responses should include a descriptive `error` field for debugging.


