import {ChangeDetectionStrategy, Component, computed, inject, signal} from '@angular/core';
import {CommonModule} from '@angular/common';
import {TableModule} from 'primeng/table';
import {ButtonModule} from 'primeng/button';
import {InputTextModule} from 'primeng/inputtext';
import {RippleModule} from 'primeng/ripple';
import {ObjectDefectsStore} from '../stores/object-defects.store';
import {DetectionResult} from '../models/detect-result.model';


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

  protected expandedRowId = signal<number | null>(null);
  protected readonly expandedRowKeys = computed(() => {
    const id = this.expandedRowId();
    return id ? {[id]: true} : {};
  });

  protected toggleRow(detection: DetectionResult) {
    console.log(`Das die Detections ${detection.id}`)
    const currentId = this.expandedRowId();
    console.log(`Das die CurrentId ${currentId}`)
    // Toggle: wenn schon expanded, dann collapse, sonst expand
    this.expandedRowId.set(currentId === detection.id ? null : detection.id);
    console.log(`Das die ExpandedRowId ${this.expandedRowId()}`)
  }

  protected isExpanded(detection: DetectionResult): boolean {
    return this.expandedRowId() === detection.id;
  }
}
