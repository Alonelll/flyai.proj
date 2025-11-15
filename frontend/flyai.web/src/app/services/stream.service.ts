import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

export interface StreamUrls {
  flv_url: string;
  hls_url: string;
  rtmp_url: string;
  player_url: string;
}

export interface StreamInfo {
  streams: any[];
}

@Injectable({
  providedIn: 'root',
})
export class StreamService {
  // Note: Als mein Frontend muss ich mich mit meinem Backend verbinden können. Daher die FastAPI url.
  private readonly httpClient = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api';

  async getStreamUrls(streamName: string = 'livestream') {
    return await firstValueFrom(
      this.httpClient.get<StreamUrls[]>(`${this.apiUrl}/stream-url`, {
        params: { stream_name: streamName },
      }),
    );
  }

  async getStreamInfo() {
    return await firstValueFrom(this.httpClient.get<StreamInfo[]>(`${this.apiUrl}/stream-info`));
  }
}
