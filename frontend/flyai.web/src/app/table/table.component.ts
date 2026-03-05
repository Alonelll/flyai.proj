import {ChangeDetectionStrategy, Component, computed, inject} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TableModule} from 'primeng/table';
import {ButtonModule} from 'primeng/button';
import {InputTextModule} from 'primeng/inputtext';
import {RippleModule} from 'primeng/ripple';
import {ObjectDefectsStore} from '../stores/object-defects.store';

@Component({
  selector: 'app-table',
  standalone: true,
  imports: [CommonModule, TableModule, ButtonModule, InputTextModule, RippleModule],
  templateUrl: 'table.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TableComponent {
  private objectDefectsStore = inject(ObjectDefectsStore);
  protected readonly detections = computed(() =>
    this.objectDefectsStore.entities().filter((x) => !!x.id && x.boxes.length > 0),
  );

  protected readonly loading = computed(() => this.objectDefectsStore.loading());
}
