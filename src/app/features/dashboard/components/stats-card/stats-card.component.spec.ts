import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CommonModule } from '@angular/common';

import { StatsCardComponent } from './stats-card.component';

describe('StatsCardComponent', () => {
  let component: StatsCardComponent;
  let fixture: ComponentFixture<StatsCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [StatsCardComponent, CommonModule],
    }).compileComponents();

    fixture = TestBed.createComponent(StatsCardComponent);
    component = fixture.componentInstance;
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should accept title input', () => {
    component.title = 'Total Users';
    expect(component.title).toBe('Total Users');
  });

  it('should accept value input as number', () => {
    component.value = 1234;
    expect(component.value).toBe(1234);
  });

  it('should accept value input as string', () => {
    component.value = '$45,678';
    expect(component.value).toBe('$45,678');
  });

  it('should accept optional icon input', () => {
    component.icon = 'fas fa-users';
    expect(component.icon).toBe('fas fa-users');
  });

  it('should accept trend input', () => {
    component.trend = 'up';
    expect(component.trend).toBe('up');

    component.trend = 'down';
    expect(component.trend).toBe('down');

    component.trend = 'neutral';
    expect(component.trend).toBe('neutral');
  });

  it('should accept trendValue input', () => {
    component.trendValue = 12.5;
    expect(component.trendValue).toBe(12.5);
  });

  it('should render title in template', () => {
    component.title = 'Revenue';
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const titleElement = compiled.querySelector('.stats-card__title');
    expect(titleElement?.textContent?.trim()).toBe('Revenue');
  });

  it('should render value in template', () => {
    component.value = 9999;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const valueElement = compiled.querySelector('.stats-card__value');
    expect(valueElement?.textContent?.trim()).toContain('9,999'); // Number pipe formatting
  });

  it('should show icon when provided', () => {
    component.icon = 'fas fa-chart-line';
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const iconElement = compiled.querySelector('.stats-card__icon');
    expect(iconElement).toBeTruthy();
  });

  it('should hide icon when not provided', () => {
    component.icon = undefined;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const iconElement = compiled.querySelector('.stats-card__icon');
    expect(iconElement).toBeFalsy();
  });

  it('should show trend when trendValue is provided', () => {
    component.trendValue = 15.5;
    component.trend = 'up';
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const trendElement = compiled.querySelector('.stats-card__trend');
    expect(trendElement).toBeTruthy();
  });

  it('should hide trend when trendValue is undefined', () => {
    component.trendValue = undefined;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const trendElement = compiled.querySelector('.stats-card__trend');
    expect(trendElement).toBeFalsy();
  });

  it('should apply correct CSS classes for trend up', () => {
    component.trend = 'up';
    component.trendValue = 10;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const trendIndicator = compiled.querySelector('.trend-indicator');
    expect(trendIndicator?.classList.contains('trend-up')).toBe(true);
  });

  it('should apply correct CSS classes for trend down', () => {
    component.trend = 'down';
    component.trendValue = -5;
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const trendIndicator = compiled.querySelector('.trend-indicator');
    expect(trendIndicator?.classList.contains('trend-down')).toBe(true);
  });
});
