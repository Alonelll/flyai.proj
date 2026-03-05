import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { DetectionSummary } from '../models/detection-summary.model';

@Injectable({ providedIn: 'root' })
export class DetectionSummaryService {
  private readonly httpClient = inject(HttpClient);
  private readonly apiUrl = '/api';

  async fetchSummary(): Promise<DetectionSummary> {
    try {
      return await firstValueFrom(
        this.httpClient.get<DetectionSummary>(`${this.apiUrl}/summary`),
      );
    } catch (error) {
      console.error('Error fetching detection summary:', error);
      throw error;
    }
  }
}

