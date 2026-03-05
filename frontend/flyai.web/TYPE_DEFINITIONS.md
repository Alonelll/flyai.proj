# TypeScript Type Definitions

Complete type definitions for the application. Reference this file when working with the API and state management.

---

## Model Interfaces

### DetectedBox
```typescript
/**
 * Represents a detected bounding box
 * Corresponds to Python API: DetectedBoxResponse
 */
export interface DetectedBox {
  id: number;           // Unique box identifier
  x1: number;          // Top-left X coordinate (pixels)
  y1: number;          // Top-left Y coordinate (pixels)
  x2: number;          // Bottom-right X coordinate (pixels)
  y2: number;          // Bottom-right Y coordinate (pixels)
  confidence: number;  // Detection confidence (0.0 - 1.0)
  class_id: number;    // Classification ID
  class_name?: string; // Human-readable class name (optional)
  tracking_id?: number; // Tracking identifier for multi-frame tracking (optional)
}
```

### DetectionResult
```typescript
/**
 * Represents a single detection result with all detected boxes
 * Corresponds to Python API: ExpectedResultResponse
 */
export interface DetectionResult {
  id: number;           // Unique result identifier
  source?: string;      // Source identifier (e.g., "camera_1")
  model_name?: string;  // Name of detection model used
  created_at?: string;  // ISO 8601 timestamp
  boxes: DetectedBox[]; // Array of detected objects
}
```

### DetectionSummary
```typescript
/**
 * Summary statistics for all detections
 * Corresponds to Python API: DetectionSummary
 */
export interface DetectionSummary {
  total_results: number;      // Total number of detection results
  total_detections: number;   // Total number of individual detections
  average_confidence: number; // Mean confidence score
  unique_classes: string[];   // List of unique class names
}
```

---

## Service Interfaces

### LazyLoadEvent
```typescript
/**
 * Event data for lazy loading in PrimeNG DataTable
 */
export interface LazyLoadEvent {
  first: number;                    // Starting index (skip)
  rows: number;                     // Page size (limit)
  sortField?: string;               // Column to sort by
  sortOrder?: 1 | -1;              // Sort direction (1 = asc, -1 = desc)
  filters?: Record<string, unknown>; // Filter criteria (extensible)
}
```

### FetchResponse
```typescript
/**
 * Standard API response for paginated results
 */
interface FetchResponse<T> {
  results: T[];    // Array of items
  total: number;   // Total count for pagination
}
```

---

## Store State Interface

### ObjectDefectsStore State
```typescript
/**
 * State managed by ObjectDefectsStore
 */
interface ObjectDefectsStoreState {
  // From withEntities<DetectionResult>()
  entities: Record<string | number, DetectionResult>;
  ids: (string | number)[];
  
  // Custom state
  loading: boolean;      // Loading state for API requests
  error: string | null;  // Error message if request fails
  totalRecords: number;  // Total records for pagination
}

/**
 * Computed signals available from store
 */
interface ObjectDefectsStoreComputed {
  entities(): DetectionResult[];
  loading(): boolean;
  error(): string | null;
  totalRecords(): number;
}

/**
 * Methods available in store
 */
interface ObjectDefectsStoreMethods {
  loadDetections(event?: LazyLoadEvent): Promise<void>;
  updateDetection(id: number, changes: Partial<DetectionResult>): Promise<void>;
  addDetectionResult(result: DetectionResult): Promise<void>;
  deleteAllDetections(): Promise<void>;
  clearError(): void;
}
```

---

## Component Interfaces

### ContentComponent
```typescript
interface ContentComponentState {
  videoPlayer: ViewChild<ElementRef<HTMLVideoElement>>;
  isVideoAvailable: Signal<boolean>;
  videoError: Signal<string | null>;
  detections: Computed<DetectionResult[]>;
}

interface ContentComponentPublic {
  // Template bindings
  isVideoAvailable: Signal<boolean>;
  videoError: Signal<string | null>;
  detections: Computed<DetectionResult[]>;
}
```

### TableComponent
```typescript
interface TableComponentState {
  detections: Computed<DetectionResult[]>;
  loading: Computed<boolean>;
  totalRecords: Computed<number>;
  expandedRows: Record<number, boolean>;
}

interface TableComponentMethods {
  onLazyLoad(event: LazyLoadEvent): void;
  toggleExpand(result: DetectionResult): void;
  isExpanded(result: DetectionResult): boolean;
}

interface TableComponentColumns {
  field: string;   // Property name
  header: string;  // Display header
  width?: string;  // Optional width
}
```

---

## Service Type Definitions

### FetchDetectsService
```typescript
@Injectable({ providedIn: 'root' })
export class FetchDetectsService {
  /**
   * Fetch paginated detection results
   * @param lazyLoadEvent Optional pagination/sorting params
   * @returns Promise resolving to results and total count
   */
  async fetchDetects(lazyLoadEvent?: LazyLoadEvent): Promise<{
    results: DetectionResult[];
    totalRecords: number;
  }>;

  /**
   * Fetch single detection result by ID
   * @param id Detection result ID
   * @returns Promise resolving to detection result or null
   */
  async fetchDetectById(id: number): Promise<DetectionResult | null>;

  /**
   * Fetch summary statistics
   * @returns Promise resolving to summary or null
   */
  async fetchDetectionSummary(): Promise<DetectionSummary | null>;
}
```

---

## API Request/Response Types

### GET /api/results Request
```typescript
interface GetResultsRequest {
  skip?: number;      // Pagination offset
  limit?: number;     // Page size
  sortField?: string; // Column to sort
  sortOrder?: 1 | -1; // Sort direction
  // Additional filter params extensible
}
```

### GET /api/results Response
```typescript
interface GetResultsResponse {
  results: DetectionResult[];
  total: number;
}
```

### GET /api/result/{id} Response
```typescript
type GetResultByIdResponse = DetectionResult | null;
```

### GET /api/summary Response
```typescript
type GetSummaryResponse = DetectionSummary;
```

### Error Response
```typescript
interface ErrorResponse {
  error: string;          // Error type/code
  message?: string;       // Detailed message
  status?: number;        // HTTP status
  timestamp?: string;     // ISO 8601 timestamp
}
```

---

## Utility Types

### Nullable
```typescript
type Nullable<T> = T | null;
type Optional<T> = T | undefined;
```

### Result Type
```typescript
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: Error };
```

### AsyncState
```typescript
interface AsyncState<T> {
  data: T | null;
  loading: boolean;
  error: Error | null;
}
```

---

## Generic Entity Types

### WithId
```typescript
interface WithId {
  id: number;
}
```

### WithTimestamp
```typescript
interface WithTimestamp {
  created_at?: string;
  updated_at?: string;
}
```

### Entity (Base Type)
```typescript
type Entity<T> = T & WithId & Partial<WithTimestamp>;
```

---

## Signal Store Types

### EntityStore
```typescript
interface EntityStore<T extends { id: number | string }> {
  // From withEntities
  entities(): T[];
  entityMap(): Record<string | number, T>;
  
  // Custom methods
  loading(): boolean;
  error(): Nullable<string>;
  
  // Store methods
  addEntity(entity: T): void;
  removeEntity(id: T['id']): void;
  updateEntity(id: T['id'], updates: Partial<T>): void;
}
```

---

## Component Decorator Types

### Component Metadata
```typescript
interface ComponentOptions {
  selector: string;
  template?: string;
  templateUrl?: string;
  styleUrls?: string[];
  styles?: string[];
  standalone?: boolean; // Always true
  imports?: any[];
  changeDetection?: ChangeDetectionStrategy;
  host?: {
    '[class]'?: string;
    '[style]'?: string;
    '(click)'?: string;
  };
}
```

---

## Form Types (For Future Use)

### FormControl
```typescript
interface FormControlState<T> {
  value: T;
  valid: boolean;
  touched: boolean;
  dirty: boolean;
  errors: ValidationErrors | null;
}
```

### ValidationErrors
```typescript
interface ValidationErrors {
  [key: string]: boolean | { [key: string]: any };
}
```

---

## Signal Types

### Signal
```typescript
interface Signal<T> {
  (): T;                          // Read value
  asReadonly(): Readonly<Signal<T>>;
}

interface WritableSignal<T> extends Signal<T> {
  set(value: T): void;           // Set value
  update(fn: (value: T) => T): void; // Update with function
}
```

### Computed
```typescript
interface Computed<T> extends Signal<T> {
  // Read-only computed property
}
```

### Effect
```typescript
function effect(
  fn: (onCleanup: (cleanup: () => void) => void) => void,
  options?: { allowSignalWrites?: boolean }
): EffectRef;
```

---

## PrimeNG Types

### PrimeNG Table Events
```typescript
interface TableDataTableLazyLoadEvent {
  first: number;
  rows: number;
  sortField?: string;
  sortOrder?: 1 | -1 | 0;
  multiSortMeta?: Array<{ field: string; order: 1 | -1 }>;
  filters?: { [s: string]: FilterMetadata };
  globalFilter?: string;
}

interface FilterMetadata {
  value: any;
  matchMode: string;
}
```

---

## HTTP Client Types

### HttpClient Methods
```typescript
interface HttpClient {
  get<T>(url: string, options?: { params: HttpParams }): Observable<T>;
  post<T>(url: string, body: any, options?: HttpOptions): Observable<T>;
  put<T>(url: string, body: any, options?: HttpOptions): Observable<T>;
  delete<T>(url: string, options?: HttpOptions): Observable<T>;
}
```

---

## Custom Type Guards

### Is Functions
```typescript
function isDetectionResult(obj: unknown): obj is DetectionResult {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'boxes' in obj
  );
}

function isDetectedBox(obj: unknown): obj is DetectedBox {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'confidence' in obj &&
    'x1' in obj &&
    'y1' in obj &&
    'x2' in obj &&
    'y2' in obj
  );
}
```

---

## Constants & Enums

### Sort Orders
```typescript
const SORT_ORDER = {
  ASC: 1 as const,
  DESC: -1 as const,
} as const;

type SortOrder = typeof SORT_ORDER[keyof typeof SORT_ORDER];
```

### Confidence Levels
```typescript
const CONFIDENCE_THRESHOLDS = {
  HIGH: 0.8,
  MEDIUM: 0.6,
  LOW: 0,
} as const;
```

### Routes
```typescript
const ROUTES = {
  HOME: '/',
  TABLE_RESULTS: '/table-results',
} as const;

type AppRoute = typeof ROUTES[keyof typeof ROUTES];
```

---

## Usage Examples

### Using Store in Component
```typescript
export class MyComponent {
  private store = inject(ObjectDefectsStore);
  
  protected detections = computed(() => {
    return this.store.entities()
      .filter(d => d.id !== undefined)
      .sort((a, b) => (b.id ?? 0) - (a.id ?? 0));
  });

  onTableLoad(event: LazyLoadEvent) {
    this.store.loadDetections(event).catch(err => {
      console.error('Failed to load:', err);
    });
  }
}
```

### Type-Safe API Call
```typescript
async function fetchData() {
  const service = inject(FetchDetectsService);
  
  try {
    const { results, totalRecords }: {
      results: DetectionResult[];
      totalRecords: number;
    } = await service.fetchDetects({
      first: 0,
      rows: 10,
      sortField: 'created_at',
      sortOrder: -1,
    });
    
    console.log(`Loaded ${results.length} of ${totalRecords}`);
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error(error.message);
    }
  }
}
```

---

**Type Definitions Complete** ✅
Use this as a reference for type-safe development.


