# FlyAI Detection API Dokumentation

## Übersicht

Die Detection API bietet Endpoints zum Speichern und Abrufen von YOLOv8 Detektionsergebnissen aus der Datenbank.

## Datenmodelle

### ExpectedResult (Detection Result)
Speichert Meta-Informationen einer Detektionssitzung:
```python
{
  "id": int,
  "source": str,          # z.B. RTMP URL oder Dateiname
  "model_name": str,      # z.B. "yolov8n"
  "created_at": datetime,
  "boxes": [BoxModel]     # Liste aller erkannten Boxen
}
```

### BoxModel (Detected Box)
Speichert einzelne erkannte Objekte (Bounding Boxes):
```python
{
  "id": int,
  "x1": float,            # Oben-links X Koordinate
  "y1": float,            # Oben-links Y Koordinate
  "x2": float,            # Unten-rechts X Koordinate
  "y2": float,            # Unten-rechts Y Koordinate
  "confidence": float,    # Confidence Score (0-1)
  "class_id": int,        # Klasse ID (z.B. 0 für Person)
  "class_name": str,      # Klasse Name (z.B. "person")
  "tracking_id": int      # Optional: Tracking ID falls objekt-tracking aktiviert
}
```

## API Endpoints

### 1. Einzelne Detection Result abrufen
```
GET /api/result/{result_id}
```
**Parameter:**
- `result_id` (int, path): Die ID der Detection Result

**Response:** `ExpectedResultResponse`
```json
{
  "id": 1,
  "source": "rtmp://fnstream.westeurope.cloudapp.azure.com/live/kassim",
  "model_name": "yolov8n",
  "created_at": "2026-03-03T10:01:38.899096",
  "boxes": [
    {
      "id": 1,
      "x1": 291.9,
      "y1": 11.4,
      "x2": 1636.8,
      "y2": 1070.5,
      "confidence": 0.938,
      "class_id": 0,
      "class_name": "person",
      "tracking_id": 1
    }
  ]
}
```

### 2. Alle Detection Results abrufen (mit Pagination und Filtern)
```
GET /api/results?skip=0&limit=10&source=&model_name=
```
**Query Parameters:**
- `skip` (int, default=0): Anzahl zu überspringender Einträge
- `limit` (int, default=10, max=100): Maximale Anzahl Ergebnisse
- `source` (str, optional): Filter nach Source URL/Name
- `model_name` (str, optional): Filter nach Model Name

**Response:** `List[ExpectedResultResponse]`

### 3. Detection Results nach Klasse filtern
```
GET /api/results/by-class/{class_id}?skip=0&limit=10
```
**Parameter:**
- `class_id` (int, path): Die Klasse ID zum Filtern
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10, max=100): Pagination limit

**Response:** `List[ExpectedResultResponse]`

### 4. High-Confidence Detektionen abrufen
```
GET /api/results/high-confidence?min_confidence=0.8&skip=0&limit=10
```
**Query Parameters:**
- `min_confidence` (float, default=0.8): Minimales Confidence Level (0-1)
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Pagination limit

**Response:** `List[ExpectedResultResponse]`

### 5. Detection Zusammenfassung (Statistiken)
```
GET /api/summary
```
**Response:** `DetectionSummary`
```json
{
  "total_results": 42,
  "total_detections": 238,
  "average_confidence": 0.87,
  "unique_classes": ["person", "car", "truck"]
}
```

## Datenbank-Struktur

### Tables
- **expected_results**: Speichert Detection Sessions
  - `id` (Primary Key)
  - `created_at` (DateTime, indexed)
  - `source` (String, indexed)
  - `model_name` (String)

- **detected_boxes**: Speichert erkannte Objekte
  - `id` (Primary Key)
  - `result_id` (Foreign Key → expected_results.id, indexed)
  - `x1, y1, x2, y2` (Float, Koordinaten)
  - `confidence` (Float)
  - `class_id` (Integer, indexed)
  - `class_name` (String)
  - `tracking_id` (Integer, optional)

## Verwendungsbeispiele

### Python mit requests
```python
import requests

# Alle Results abrufen
response = requests.get("http://localhost:8000/api/results?limit=5")
results = response.json()

# Spezifische Result abrufen
response = requests.get("http://localhost:8000/api/result/1")
result = response.json()

# High-Confidence Results
response = requests.get("http://localhost:8000/api/results/high-confidence?min_confidence=0.9")
high_conf = response.json()

# Summary
response = requests.get("http://localhost:8000/api/summary")
summary = response.json()
print(f"Total Detections: {summary['total_detections']}")
print(f"Average Confidence: {summary['average_confidence']}")
```

### cURL
```bash
# Alle Results
curl "http://localhost:8000/api/results"

# Nach Klasse filtern
curl "http://localhost:8000/api/results/by-class/0"

# High-Confidence
curl "http://localhost:8000/api/results/high-confidence?min_confidence=0.85"

# Summary
curl "http://localhost:8000/api/summary"
```

## Fehlerbehandlung

### 404 Not Found
```json
{
  "detail": "Detection result {id} not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["query", "limit"],
      "msg": "ensure this value is less than or equal to 100",
      "type": "value_error.number.not_le"
    }
  ]
}
```

## Service-Architektur

```
┌─────────────────────────────────────┐
│    FastAPI Router (router.py)       │
│    - HTTP Endpoints                 │
│    - Request/Response Handling      │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  DetectionResultService             │
│    - Business Logic                 │
│    - Database Queries               │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Database Layer (AsyncSessionLocal) │
│    - SQLAlchemy ORM                 │
│    - PostgreSQL Async Driver        │
└─────────────────────────────────────┘
```

## Performance-Tipps

1. **Pagination verwenden**: Limit bei großen Datenmengen immer setzen
2. **Indizes nutzen**: `created_at`, `class_id`, und `result_id` sind indexed
3. **Filtering**: Filter nach Source/Model vor Pagination für bessere Performance
4. **Caching**: Für Summary-Endpoint könnte Caching implementiert werden

