import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-card.component.html',
  styleUrl: './stats-card.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class StatsCardComponent {
  @Input() title!: string;
  @Input() value!: number | string;
  @Input() icon?: string;
  @Input() trend?: 'up' | 'down' | 'neutral';
  @Input() trendValue?: number;
}
