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

  //ToDo: RTMP stream URL should be configurable
  async initFlvPlayer() {
    const streamUrl = 'http://localhost:8080/live/livestream.flv';
    const videoElement = document.getElementById('liveVideo') as HTMLVideoElement;
    if (streamUrl && flvjs.isSupported() && videoElement) {
      const player = flvjs.createPlayer({
        type: 'flv',
        url: streamUrl
      });
      player.attachMediaElement(videoElement);
      player.load();
      player.play();
    }
  }

  async ngAfterViewInit() {
    await this.initFlvPlayer();
  }

  onCancel() {
    console.log('Cancel button clicked');
  }
}
