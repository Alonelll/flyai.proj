# Architecture Overview

## Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Angular Application                      │
│                    (Standalone Components)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                │                            │
        ┌───────▼────────┐        ┌──────────▼──────┐
        │  App Component │        │  App Routes     │
        │   (Root)       │        │                 │
        └───────┬────────┘        └──────┬──────────┘
                │                        │
        ┌───────▼────────┐        ┌──────▼──────────┐
        │  NavBar        │        │  Route Resolver │
        │  (Global)      │        │                 │
        └────────────────┘        └──────┬──────────┘
                │                        │
                └────────┬───────────────┘
                         │
            ┌────────────▼──────────────┐
            │   Router Outlet           │
            │   (Page Container)        │
            └────────┬───────────────┬──┘
                     │               │
            ┌────────▼────┐  ┌───────▼──────┐
            │   Content   │  │   Table      │
            │  Component  │  │  Component   │
            │  (Live View)│  │  (Results)   │
            └────────┬────┘  └───────┬──────┘
                     │               │
        ┌────────────▼───┐  ┌────────▼────────┐
        │ Video Renderer │  │ PrimeNG DataTable
        │ (FLV.js)       │  │ (LazyLoading)   │
        └────────┬───────┘  └────────┬────────┘
                 │                   │
                 └────────┬──────────┘
                          │
              ┌───────────▼──────────┐
              │  Object Defects      │
              │  Store (@ngrx/signals)
              │  (State Management)  │
              └───────────┬──────────┘
                          │
          ┌───────────────▼──────────────┐
          │                              │
     ┌────▼──────────┐      ┌───────────▼────┐
     │ HTTP Client   │      │ Fetch Service  │
     │ (Angular)     │      │ (API Layer)    │
     └────┬──────────┘      └───────────┬────┘
          │                             │
          └─────────────┬───────────────┘
                        │
                 ┌──────▼──────┐
                 │  Backend    │
                 │  API Server │
                 │  (/api)     │
                 └─────────────┘
```

---

## Component Hierarchy

```
App (Root Component)
├── NavbarComponent
│   └── RouterLink/RouterLinkActive
│       ├── Link: "/" → ContentComponent
│       └── Link: "/table-results" → TableComponent
│
└── RouterOutlet
    ├── ContentComponent (Route: "")
    │   ├── Video Element
    │   ├── PrimeNG Message (Errors)
    │   └── [Injected] ObjectDefectsStore
    │
    └── TableComponent (Route: "table-results", Lazy Loaded)
        ├── PrimeNG DataTable
        │   ├── Header Row (Sortable Columns)
        │   ├── Data Rows (Expandable)
        │   ├── Expanded Row (Boxes Details)
        │   └── Footer (Pagination)
        └── [Injected] ObjectDefectsStore
```

---

## State Management Architecture

```
┌─────────────────────────────────────┐
│  ObjectDefectsStore (@ngrx/signals) │
│                                     │
│  State:                             │
│  ├── entities: DetectionResult[]    │
│  ├── loading: boolean               │
│  ├── error: string | null           │
│  └── totalRecords: number           │
│                                     │
│  Methods:                           │
│  ├── loadDetections(event?)         │
│  ├── updateDetection(id, changes)   │
│  ├── addDetectionResult(item)       │
│  ├── deleteAllDetections()          │
│  └── clearError()                   │
│                                     │
│  Hooks:                             │
│  └── onInit() → loadDetections()    │
└────────────┬────────────────────────┘
             │
    ┌────────▼─────────┐
    │ Computed Signals │
    ├─ detections()    │
    ├─ loading()       │
    └─ totalRecords()  │
             │
    ┌────────▼──────────────────┐
    │ Used in Components         │
    ├── ContentComponent         │
    └── TableComponent           │
```

---

## Data Flow (Table Lazy Loading)

```
User scrolls/changes page
        │
        ▼
TableComponent.onLazyLoad(event)
  - first: 10
  - rows: 10
  - sortField: 'created_at'
  - sortOrder: -1
        │
        ▼
ObjectDefectsStore.loadDetections(event)
        │
        ├─ patchState({ loading: true })
        │
        ▼
FetchDetectsService.fetchDetects(event)
        │
        ▼
HttpClient.get('/api/results?skip=10&limit=10...')
        │
        ▼
Backend API Response
        │
        ├─ results: DetectionResult[]
        └─ total: 150
        │
        ▼
ObjectDefectsStore
  ├─ setAllEntities(results)
  ├─ patchState({ loading: false, totalRecords: 150 })
        │
        ▼
Computed Properties Updated
  ├─ detections() → new array
  ├─ loading() → false
  └─ totalRecords() → 150
        │
        ▼
TableComponent (OnPush detection)
        │
        ▼
Template Re-renders with New Data
```

---

## API Integration Points

```
┌──────────────────────────────────────┐
│     Frontend Application              │
│                                      │
│  ┌──────────────────────────────┐   │
│  │   FetchDetectsService        │   │
│  │                              │   │
│  │  Methods:                    │   │
│  │  ├─ fetchDetects()           │   │
│  │  │  GET /api/results?...     │   │
│  │  │                           │   │
│  │  ├─ fetchDetectById(id)      │   │
│  │  │  GET /api/result/{id}     │   │
│  │  │                           │   │
│  │  └─ fetchDetectionSummary()  │   │
│  │     GET /api/summary         │   │
│  └──────────────┬───────────────┘   │
└─────────────────┼───────────────────┘
                  │
                  │ HTTP Requests
                  │
┌─────────────────▼───────────────────┐
│   Backend API Server                 │
│   (Python FastAPI / Django)          │
│                                      │
│   Endpoints:                         │
│   ├─ GET /api/results                │
│   ├─ GET /api/result/{id}            │
│   └─ GET /api/summary                │
│                                      │
│   Database:                          │
│   ├─ DetectionResults table          │
│   └─ DetectedBoxes table             │
└──────────────────────────────────────┘
```

---

## Model Relationships

```
DetectionResult (Parent)
├── id: number
├── source?: string
├── model_name?: string
├── created_at?: string
│
└── boxes: DetectedBox[] (Child)
    ├── id: number
    ├── x1, y1, x2, y2: number
    ├── confidence: number (0.0-1.0)
    ├── class_id: number
    ├── class_name?: string
    └── tracking_id?: number

DetectionSummary (Statistics)
├── total_results: number
├── total_detections: number
├── average_confidence: number
└── unique_classes: string[]
```

---

## Module Dependencies

```
Core Modules:
├── @angular/core
├── @angular/router
├── @angular/common
└── @angular/platform-browser

State Management:
├── @ngrx/signals
└── @ngrx/signals/entities

UI Framework:
├── primeng (DataTable, Button, Message, etc.)
├── primeicons (Icons)
├── tailwindcss (Styling)

Media:
└── flv.js (FLV Stream Playback)
```

---

## Change Detection Strategy

All components use **OnPush** change detection:

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
```

This optimizes performance by:
- Only checking when @Input changes or events fire
- Using Signals for automatic tracking
- Reducing unnecessary change detection cycles

---

## Error Handling Flow

```
API Request Error
        │
        ▼
FetchDetectsService (try-catch)
        │
        ├─ Success → return { results, total }
        │
        └─ Error → throw error
                   │
        ▼
Store.loadDetections() (try-catch)
        │
        ├─ Success → patchState(results)
        │
        └─ Error → patchState({ error: message })
                   │
        ▼
Component (computed)
        │
        ├─ Detect error signal
        │
        ├─ Render error message
        │
        └─ German: "Serververbindung verloren..."
```

---

## Build & Deployment

```
Source Code
    │
    ▼
npm run build
    │
    ├─ TypeScript compilation
    ├─ Tree shaking
    ├─ Code splitting (lazy routes)
    ├─ CSS bundling (Tailwind, PrimeNG)
    │
    ▼
dist/flyai.web/
    │
    ├─ index.html (Entry point)
    ├─ main-*.js (App code)
    ├─ chunk-*.js (Lazy loaded modules)
    ├─ polyfills-*.js
    ├─ styles-*.css
    └─ favicon.ico
    │
    ▼
Deploy to Web Server
    (Nginx, Apache, etc.)
```

---

## Performance Optimizations Applied

✅ **OnPush Change Detection**
- Reduces unnecessary re-renders

✅ **Lazy Loading Routes**
- Code split at route boundaries
- Smaller initial bundle

✅ **Signals & Computed**
- Fine-grained reactivity
- No dirty checking

✅ **Standalone Components**
- Tree-shakeable
- No module overhead

✅ **Image Optimization**
- Using NgOptimizedImage (when applicable)

✅ **PrimeNG Lazy Tables**
- Virtual scrolling support
- Paginated data loading

---

**Architecture Complete** ✅
Ready for development and deployment!


