import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ContentComponent } from './content/content.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ContentComponent],
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('flyai.web');
}
