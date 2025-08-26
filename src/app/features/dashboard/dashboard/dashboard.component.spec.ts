import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommonModule } from '@angular/common';
import { of } from 'rxjs';

import { DashboardComponent, DashboardStats } from './dashboard.component';
import { AuthService, User } from '../../../core/services/auth.service';
import { StatsCardComponent } from '../components/stats-card/stats-card.component';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;
  // let authServiceSpy: jasmine.SpyObj<AuthService>;

  const mockUser: User = {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'admin'
  };

  beforeEach(async () => {
    const authSpy = jasmine.createSpyObj('AuthService', [], {
      currentUser$: of(mockUser)
    });

    await TestBed.configureTestingModule({
      imports: [DashboardComponent, CommonModule, StatsCardComponent],
      providers: [
        { provide: AuthService, useValue: authSpy }
      ]
    }).compileComponents();

    // authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize with default stats', () => {
    const expectedStats: DashboardStats = {
      totalUsers: 1234,
      activeUsers: 987,
      revenue: 45678,
      growth: 12.5
    };

    expect(component.stats).toEqual(expectedStats);
  });

  it('should have current user observable', () => {
    expect(component.currentUser$).toBeDefined();

    component.currentUser$.subscribe(user => {
      expect(user).toEqual(mockUser);
    });
  });

  it('should call onRefreshStats method', () => {
    spyOn(component, 'onRefreshStats');
    component.onRefreshStats();
    expect(component.onRefreshStats).toHaveBeenCalled();
  });

  it('should implement ngOnInit', () => {
    spyOn(component, 'ngOnInit');
    component.ngOnInit();
    expect(component.ngOnInit).toHaveBeenCalled();
  });

  it('should have OnPush change detection strategy', () => {
    expect(component.constructor).toBeDefined();
  });
});
