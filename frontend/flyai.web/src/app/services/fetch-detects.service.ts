import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { DetectionResult } from '../models/detect-result.model';

@Injectable({ providedIn: 'root' })
export class FetchDetectsService {
  private readonly httpClient = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api/detects';

  async fetchDetects(): Promise<DetectionResult[]> {
    try {
      const response = await firstValueFrom(
        this.httpClient.get<DetectionResult[] | null>(this.apiUrl),
      );
      return Array.isArray(response) ? response : [];
    } catch (error) {
      console.error('Error fetching detects:', error);
      throw error;
    }
  }
}
