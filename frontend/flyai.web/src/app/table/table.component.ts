import { ChangeDetectionStrategy, Component, computed, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TableModule } from 'primeng/table';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { RippleModule } from 'primeng/ripple';
import { ObjectDefectsStore } from '../stores/object-defects.store';
import { DetectionResult } from '../models/detect-result.model';

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
    this.objectDefectsStore.entities().filter((x) => !!x.id),
  );

  protected readonly loading = computed(() => this.objectDefectsStore.loading());

  protected columns = [
    { field: 'id', header: 'ID', width: '60px' },
    { field: 'model_name', header: 'Model', width: '150px' },
    { field: 'source', header: 'Source', width: '200px' },
    { field: 'created_at', header: 'Created At', width: '180px' },
  ];

  protected detailColumns = [
    { field: 'id', header: 'Box ID' },
    { field: 'class_name', header: 'Class' },
    { field: 'confidence', header: 'Confidence' },
    { field: 'x1', header: 'X1' },
    { field: 'y1', header: 'Y1' },
    { field: 'x2', header: 'X2' },
    { field: 'y2', header: 'Y2' },
  ];

  protected expandedRows: Record<number, boolean> = {};

  toggleExpand(result: DetectionResult): void {
    const id = result.id;
    this.expandedRows[id] = !this.expandedRows[id];
  }

  isExpanded(result: DetectionResult): boolean {
    return this.expandedRows[result.id] ?? false;
  }
}
