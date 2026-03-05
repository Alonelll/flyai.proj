import { inject } from '@angular/core';
import { patchState, signalStore, withHooks, withMethods, withState } from '@ngrx/signals';
import { DetectionSummary } from '../models/detection-summary.model';
import { DetectionSummaryService } from '../services/detection-summary.service';

export const DetectionSummaryStore = signalStore(
  { providedIn: 'root' },
  withState({
    summary: null as DetectionSummary | null,
    loading: false,
    error: null as string | null,
  }),
  withMethods((store) => {
    const detectionSummaryService = inject(DetectionSummaryService);

    return {
      async load() {
        patchState(store, { loading: true, error: null });
        try {
          const summary = await detectionSummaryService.fetchSummary();
          patchState(store, { summary });
        } catch (error) {
          const message = error instanceof Error ? error.message : 'Failed to load summary';
          patchState(store, { error: message });
        } finally {
          patchState(store, { loading: false });
        }
      },

      clear() {
        patchState(store, { summary: null, error: null });
      },
    };
  }),
  withHooks({
    onInit(store) {
      store.load();
    },
  })
);

