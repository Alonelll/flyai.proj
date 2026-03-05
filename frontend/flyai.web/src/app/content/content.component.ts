import { Component, ElementRef, effect, viewChild, computed, inject, signal, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MessageModule } from 'primeng/message';
import FlvJs from 'flv.js';
import { ObjectDefectsStore } from '../stores/object-defects.store';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [CommonModule, MessageModule],
  templateUrl: './content.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ContentComponent {
  videoPlayer = viewChild('videoRef', { read: ElementRef<HTMLVideoElement> });
  private objectDefectsStore = inject(ObjectDefectsStore);
  protected readonly detections = computed(() =>
    this.objectDefectsStore.entities().filter((x) => !!x.id),
  );

  protected readonly isVideoAvailable = signal(true);
  protected readonly videoError = signal<string | null>(null);

  constructor() {
    console.log(this.detections());
    effect((onCleanup) => {
      const videoElement = this.videoPlayer()?.nativeElement;

      if (!videoElement) {
        return;
      }

      if (!FlvJs.isSupported()) {
        this.isVideoAvailable.set(false);
        this.videoError.set('Video playback is not supported in this browser');
        return;
      }

      this.isVideoAvailable.set(true);
      this.videoError.set(null);

      try {
        const flvPlayer = FlvJs.createPlayer({
          type: 'flv',
          url: 'http://fnstream.westeurope.cloudapp.azure.com:8080/live/output.flv',
        });

        flvPlayer.attachMediaElement(videoElement);
        flvPlayer.load();
        const playResult = flvPlayer.play();
        if (playResult instanceof Promise) {
          playResult.catch((error: unknown) => {
            console.error('Error playing video:', error);
            this.videoError.set('Serververbindung verloren oder Stream Offline');
            this.isVideoAvailable.set(false);
          });
        }

        onCleanup(() => {
          try {
            flvPlayer.destroy();
          } catch (error) {
            console.error('Error destroying FLV player:', error);
          }
        });
      } catch (error) {
        console.error('Error initializing FLV player:', error);
        this.videoError.set('Serververbindung verloren oder Stream Offline');
        this.isVideoAvailable.set(false);
      }
    });
  }
}
