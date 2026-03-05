# Quick Start Guide

## Project Status ✅

Your Angular 20 frontend is now fully configured with:
- ✅ Dynamic PrimeNG table with lazy loading
- ✅ Refactored models matching Python API
- ✅ Signal-based state management (ObjectDefectsStore)
- ✅ Video streaming with error handling
- ✅ Global navigation bar
- ✅ Responsive design with Tailwind CSS

---

## Running the Project

### Development Server
```bash
npm start
```
Opens at: `http://localhost:4200`

### Production Build
```bash
npm run build
```
Output: `dist/flyai.web`

### Run Tests
```bash
npm run test
```

---

## File Structure

```
src/app/
├── app.ts                          # Root component
├── app.html                        # Root template
├── app.routes.ts                   # Route configuration
├── app.config.ts                   # App providers
│
├── navbar/
│   ├── navbar.component.ts         # Navigation component
│   └── navbar.component.html       # Navbar template
│
├── content/
│   ├── content.component.ts        # Video streaming
│   ├── content.component.html      # Video template
│   └── content.component.css       # Video styles
│
├── table/
│   ├── table.component.ts          # Results table
│   └── table.component.html        # Table template (PrimeNG)
│
├── models/
│   ├── bounding-box.model.ts       # DetectedBox interface
│   ├── detect-result.model.ts      # DetectionResult interface
│   ├── detection-summary.model.ts  # DetectionSummary interface
│   └── ...                         # Other models
│
├── services/
│   └── fetch-detects.service.ts    # API service with lazy loading
│
└── stores/
    └── object-defects.store.ts     # Signal store (ngrx/signals)
```

---

## Key Features

### 1. Dynamic Table Component
**Location**: `src/app/table/table.component.ts`

Features:
- Lazy loading with pagination
- Sortable columns
- Expandable rows showing detected boxes
- Confidence color coding
- Checkbox selection

Usage:
```typescript
// Table auto-loads on route navigation
// Paginate/sort via PrimeNG table events
```

### 2. Signal Store (State Management)
**Location**: `src/app/stores/object-defects.store.ts`

Usage in components:
```typescript
export class MyComponent {
  private store = inject(ObjectDefectsStore);
  
  // Computed properties
  protected detections = computed(() => this.store.entities());
  protected loading = computed(() => this.store.loading());
  
  // Methods
  loadMore(event: LazyLoadEvent) {
    this.store.loadDetections(event);
  }
}
```

### 3. API Service with Lazy Loading
**Location**: `src/app/services/fetch-detects.service.ts`

Usage:
```typescript
// With pagination
const { results, totalRecords } = await fetchDetectsService.fetchDetects({
  first: 0,
  rows: 10,
  sortField: 'created_at',
  sortOrder: -1
});

// Get summary
const summary = await fetchDetectsService.fetchDetectionSummary();
```

### 4. Video Streaming with Error Handling
**Location**: `src/app/content/content.component.ts`

Features:
- FLV stream playback
- Error detection with German message: "Serververbindung verloren oder Stream Offline"
- Graceful fallback UI
- Auto-cleanup on navigation

---

## Backend API Integration

### Expected Endpoints
1. `GET /api/results` - Paginated detection results
2. `GET /api/result/{id}` - Single result
3. `GET /api/summary` - Summary statistics

### Request Example
```typescript
// The service handles this automatically
GET /api/results?skip=0&limit=10&sortField=created_at&sortOrder=-1
```

### Response Structure
```json
{
  "results": [
    {
      "id": 1,
      "model_name": "YOLOv8",
      "source": "camera_1",
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
          "class_name": "person"
        }
      ]
    }
  ],
  "total": 150
}
```

See `API_CONTRACT.md` for complete API specification.

---

## Angular Best Practices Applied

✅ **Standalone Components**
- All components use `standalone: true`
- Modular and tree-shakeable

✅ **Signals & Computed**
```typescript
protected detections = signal([]);
protected loading = signal(false);
protected filtered = computed(() => 
  this.detections().filter(d => d.id)
);
```

✅ **Change Detection OnPush**
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush,
  // ...
})
```

✅ **No Deprecated Features**
- ❌ No `@HostBinding`, `@HostListener`
- ❌ No `ngClass`, `ngStyle` (use class bindings)
- ❌ No `*ngIf`, `*ngFor` (use `@if`, `@for`)
- ❌ No `any` types

✅ **Proper Dependency Injection**
```typescript
export class MyComponent {
  private service = inject(MyService); // Functional injection
}
```

---

## Troubleshooting

### Video Stream Not Loading
1. Check FLV stream URL in `content.component.ts`
2. Verify server is running: `http://fnstream.westeurope.cloudapp.azure.com:8080/live/output.flv`
3. Check browser console for errors
4. Verify CORS headers if needed

### Table Shows No Data
1. Verify backend API is running
2. Check Network tab for API response
3. Ensure response matches `API_CONTRACT.md`
4. Check store state: `store.entities()` should have data

### Build Errors
1. Delete `node_modules` and `dist` folders
2. Run: `npm install --legacy-peer-deps`
3. Run: `npm run build`

---

## Next Steps

1. **Connect to Backend**
   - Update proxy config in `proxy.conf.json` if needed
   - Test API endpoints

2. **Customize Table**
   - Add filters
   - Change page size
   - Adjust column widths

3. **Customize Theme**
   - Change PrimeNG theme in `angular.json`
   - Available themes: `lara-light-blue`, `lara-dark-blue`, etc.

4. **Add Authentication** (if needed)
   - Implement JWT interceptor
   - Add login page

---

## Support Files

- `CHANGES_SUMMARY.md` - Detailed changelog
- `API_CONTRACT.md` - Backend API specification
- `README.md` - Original project README

---

## Package Versions

```json
{
  "@angular/core": "^20.2.0",
  "@ngrx/signals": "^21.0.1",
  "primeng": "^20.0.1",
  "primeicons": "^7.0.0",
  "tailwindcss": "^3.x"
}
```

---

**Last Updated**: March 5, 2026
**Status**: Ready for Backend Integration ✅


