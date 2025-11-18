import {AfterViewInit, Component, inject} from '@angular/core';
import {ButtonModule} from 'primeng/button';
import {FormsModule} from '@angular/forms';
import flvjs from 'flv.js';
import {Skeleton} from 'primeng/skeleton';

@Component({
  selector: 'app-content',
  imports: [ButtonModule, FormsModule, Skeleton],
  templateUrl: './content.component.html',
})
export class ContentComponent implements AfterViewInit {

  private flvPlayer: flvjs.Player | null = null;

  // TODO: RTMP stream URL should be configurable
  initFlvPlayer() {
    const streamUrl = 'http://localhost:8080/live/livestream.flv';
    const videoElement = document.getElementById('liveVideo') as HTMLVideoElement;
    if (streamUrl && flvjs.isSupported() && videoElement) {
      // Destroy previous player if exists
      if (this.flvPlayer) {
        this.flvPlayer.destroy();
        this.flvPlayer = null;
      }
      this.flvPlayer = flvjs.createPlayer({
        type: 'flv',
        url: streamUrl
      });
      this.flvPlayer.attachMediaElement(videoElement);
      this.flvPlayer.load();
      this.flvPlayer.play();
    }
  }

  async ngAfterViewInit() {
    await this.initFlvPlayer();
  }

  onCancel() {
    console.log('Cancel button clicked');
  }
}
