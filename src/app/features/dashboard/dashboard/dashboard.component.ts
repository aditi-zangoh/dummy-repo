import { Component, OnInit, ChangeDetectionStrategy, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Observable } from 'rxjs';
import { AuthService, User } from '../../../core/services/auth.service';
import { StatsCardComponent } from '../components/stats-card/stats-card.component';

export interface DashboardStats {
  totalUsers: number;
  activeUsers: number;
  revenue: number;
  growth: number;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCardComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardComponent implements OnInit {
  currentUser$: Observable<User | null>;
  stats: DashboardStats = {
    totalUsers: 1234,
    activeUsers: 987,
    revenue: 45678,
    growth: 12.5,
  };

  private authService = inject(AuthService);

  constructor() {
    this.currentUser$ = this.authService.currentUser$;
  }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  private loadDashboardData(): void {
    // Load actual dashboard statistics from service
    console.log('Loading dashboard data...');
  }

  onRefreshStats(): void {
    // Refresh dashboard statistics
  }
}
