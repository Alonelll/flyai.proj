import { Component, computed, inject } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { FormsModule } from '@angular/forms';
import { StreamService } from '../services/stream.service';

@Component({
  selector: 'app-content',
  imports: [ButtonModule, FormsModule],
  templateUrl: './content.component.html',
})
export class ContentComponent {
  protected readonly streamService = inject(StreamService);
  protected readonly stream = computed(() => {
    const streamInfos = this.streamService.getStreamInfo();
    const streamUrls = this.streamService.getStreamUrls();

    console.log('Stream Infos:', streamInfos);
    console.log('Stream URLs:', streamUrls);

    return {
      infos: streamInfos,
      urls: streamUrls,
    };
  });

  onSubmit() {
    const rtmp = '';
    console.log('Submit button clicked with RTMP URL:', rtmp);
  }

  onCancel() {
    console.log('Cancel button clicked');
  }
}
