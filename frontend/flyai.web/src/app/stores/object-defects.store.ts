import { inject } from '@angular/core';
import {
  patchState,
  signalStore,
  withHooks,
  withMethods,
  withState,
} from '@ngrx/signals';
import {
  setAllEntities,
  setEntity,
  updateEntity,
  withEntities,
} from '@ngrx/signals/entities';
import { FetchDetectsService } from '../services/fetch-detects.service';
import { DetectionResult } from '../models/detect-result.model';

export const ObjectDefectsStore = signalStore(
  { providedIn: 'root' },
  withEntities<DetectionResult>(),
  withState({
    loading: false,
    loadingIds: new Set<string>(),
  }),

  withMethods((store) => {
    const fetchDetectsService = inject(FetchDetectsService);

    const _startLoading = (id: string) => {
      const tmp = store.loadingIds();
      tmp.add(id);
      patchState(store, { loading: tmp.has('all'), loadingIds: tmp });
    };

    const _stopLoading = (id: string) => {
      const tmp = store.loadingIds();
      tmp.delete(id);
      patchState(store, { loading: tmp.has('all'), loadingIds: tmp });
    };

    return {
      async load() {
        _startLoading('all');
        try {
          const defectResults = await fetchDetectsService.fetchDetects();
          patchState(store, setAllEntities(defectResults ?? []));
        } finally {
          _stopLoading('all');
        }
      },

      async update(id: string, changes: Partial<DetectionResult>) {
        _startLoading(id);
        try {
          // Update logic here if needed
          patchState(store, updateEntity({ id, changes }));
        } finally {
          _stopLoading(id);
        }
      },

      async deleteAll() {
        patchState(store, setAllEntities<DetectionResult>([]));
      },

      async addDefectResult(defectResult: DetectionResult) {
        patchState(store, setEntity(defectResult));
      },
    };
  }),

  withHooks({
    onInit(store) {
      store.load();
    },
  })
);
