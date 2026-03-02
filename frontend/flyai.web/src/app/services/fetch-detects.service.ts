import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class FetchDetectsService {
  public httpClient = inject(HttpClient);
  public apiUrl = 'http://localhost:8000/api/detects';
  constructor() {}

  async fetchDetects() {
    try {
      const response = await firstValueFrom(this.httpClient.get('/api/detects'));
      console.log('Fetched detects:', response);
      return response;
    } catch (error) {
      console.error('Error fetching detects:', error);
      throw error;
    }
  }
}
