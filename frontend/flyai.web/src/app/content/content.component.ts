import {Component, ElementRef, effect, viewChild, computed, inject} from '@angular/core';
import FlvJs from 'flv.js';
import {ObjectDefectsStore} from '../stores/object-defects.store';

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
})
export class ContentComponent {
  videoPlayer = viewChild('videoRef', {read: ElementRef<HTMLVideoElement>});
  private objectDefectsStore = inject(ObjectDefectsStore);
  protected readonly detections = computed(() =>
    this.objectDefectsStore.entities().filter(x => !!x.id)
  );

  constructor() {
    console.log(this.detections());
    effect((onCleanup) => {
      const flvPlayer = FlvJs.createPlayer({
        type: 'flv',
        url: 'http://fnstream.westeurope.cloudapp.azure.com:8080/live/output.flv',
      });
      flvPlayer.attachMediaElement(this.videoPlayer()?.nativeElement);
      flvPlayer.load();
      flvPlayer.play();
      onCleanup(() => flvPlayer.destroy())
      return;
    });
  }
}

// effect((onCleanup) => {

//   const video = this.videoPlayer()?.nativeElement;
//   console.log(video);
//
//   if (!video) return;
//
//   const url = '/live/output.m3u8';
//
//   if (Hls.isSupported()) {
//     const hls = new Hls({ liveSyncDurationCount: 3, liveMaxLatencyDurationCount: 6 });
//     hls.loadSource(url);
//     hls.attachMedia(video);
//     hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
//     onCleanup(() => hls.destroy());
//     return;
//   }
//
//   // Check ob Browser HLS untersrtützt
//   if (video.canPlayType('application/vnd.apple.mpegurl')) {
//     video.src = url;
//     video.onloadedmetadata = () => video.play();
//   } else {
//     const hls = new Hls();
//     hls.loadSource(url);
//     hls.attachMedia(video);
//     hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
//   }
// });
