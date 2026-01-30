import { Component, ElementRef, effect, viewChild } from '@angular/core';
import Hls from 'hls.js';

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
})
export class ContentComponent {
  videoPlayer = viewChild('videoRef', { read: ElementRef<HTMLVideoElement> });

  constructor() {
    effect((onCleanup) => {
      const video = this.videoPlayer()?.nativeElement;
      if (!video) return;

      const url = '/live/output.m3u8';

      if (Hls.isSupported()) {
        const hls = new Hls({ liveSyncDurationCount: 3, liveMaxLatencyDurationCount: 6 });
        hls.loadSource(url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
        onCleanup(() => hls.destroy());
        return;
      }

      // Check ob Browser HLS untersrtützt
      if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = url;
        video.onloadedmetadata = () => video.play();
      } else {
        const hls = new Hls();
        hls.loadSource(url);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
      }
    });
  }
}
