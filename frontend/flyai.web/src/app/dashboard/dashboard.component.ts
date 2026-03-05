import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardModule } from 'primeng/card';
import { SkeletonModule } from 'primeng/skeleton';
import { MessageModule } from 'primeng/message';
import { ChipModule } from 'primeng/chip';
import { ChartModule } from 'primeng/chart';
import { DetectionSummaryStore } from '../stores/detection-summary.store';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, CardModule, SkeletonModule, MessageModule, ChipModule, ChartModule],
  templateUrl: './dashboard.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent {
  private summaryStore = inject(DetectionSummaryStore);

  protected readonly summary = computed(() => this.summaryStore.summary());
  protected readonly loading = computed(() => this.summaryStore.loading());
  protected readonly error = computed(() => this.summaryStore.error());

  protected readonly averageConfidencePercentage = computed(() => {
    const sum = this.summary();
    return sum ? (sum.average_confidence * 100).toFixed(1) : '0.0';
  });

  protected readonly confidenceColor = computed(() => {
    const sum = this.summary();
    if (!sum) return 'text-slate-600';
    if (sum.average_confidence >= 0.8) return 'text-green-600';
    if (sum.average_confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  });

  protected readonly confidenceBgColor = computed(() => {
    const sum = this.summary();
    if (!sum) return 'bg-slate-100';
    if (sum.average_confidence >= 0.8) return 'bg-green-50';
    if (sum.average_confidence >= 0.6) return 'bg-yellow-50';
    return 'bg-red-50';
  });

  protected readonly chartData = computed(() => {
    const sum = this.summary();
    if (!sum) return null;

    return {
      labels: sum.unique_classes,
      datasets: [
        {
          label: 'Erkannte Klassen',
          data: sum.unique_classes.map(() => Math.floor(Math.random() * 100) + 1),
          backgroundColor: [
            'rgba(99, 102, 241, 0.8)',
            'rgba(59, 130, 246, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(236, 72, 153, 0.8)',
            'rgba(249, 115, 22, 0.8)',
            'rgba(234, 179, 8, 0.8)',
            'rgba(34, 197, 94, 0.8)',
            'rgba(20, 184, 166, 0.8)',
          ],
          borderColor: [
            'rgb(99, 102, 241)',
            'rgb(59, 130, 246)',
            'rgb(139, 92, 246)',
            'rgb(236, 72, 153)',
            'rgb(249, 115, 22)',
            'rgb(234, 179, 8)',
            'rgb(34, 197, 94)',
            'rgb(20, 184, 166)',
          ],
          borderWidth: 2,
        },
      ],
    };
  });

  protected readonly chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            return `${context.label}: ${context.parsed.y}`;
          },
        },
      },
    },
  };

  protected readonly confidenceGaugeData = computed(() => {
    const sum = this.summary();
    if (!sum) return null;

    const confidence = sum.average_confidence * 100;
    return {
      labels: ['Vertrauen', 'Verbleibend'],
      datasets: [
        {
          data: [confidence, 100 - confidence],
          backgroundColor: [
            confidence >= 80 ? 'rgb(34, 197, 94)' : confidence >= 60 ? 'rgb(234, 179, 8)' : 'rgb(239, 68, 68)',
            'rgb(229, 231, 235)',
          ],
          borderWidth: 0,
        },
      ],
    };
  });

  protected readonly gaugeOptions = {
    responsive: true,
    maintainAspectRatio: false,
    circumference: 180,
    rotation: -90,
    cutout: '75%',
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        enabled: false,
      },
    },
  };
}

