import { TestBed } from '@angular/core/testing';

import { NotificationService } from './notification.service';

describe('NotificationService', () => {
  let service: NotificationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NotificationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should show success message', () => {
    spyOn(console, 'log');

    service.showSuccess('Test success message');

    expect(console.log).toHaveBeenCalledWith('Success:', 'Test success message');
  });

  it('should show error message', () => {
    spyOn(console, 'error');

    service.showError('Test error message');

    expect(console.error).toHaveBeenCalledWith('Error:', 'Test error message');
  });

  it('should show warning message', () => {
    spyOn(console, 'warn');

    service.showWarning('Test warning message');

    expect(console.warn).toHaveBeenCalledWith('Warning:', 'Test warning message');
  });

  it('should handle empty messages', () => {
    spyOn(console, 'log');
    spyOn(console, 'error');
    spyOn(console, 'warn');

    service.showSuccess('');
    service.showError('');
    service.showWarning('');

    expect(console.log).toHaveBeenCalledWith('Success:', '');
    expect(console.error).toHaveBeenCalledWith('Error:', '');
    expect(console.warn).toHaveBeenCalledWith('Warning:', '');
  });

  it('should handle multiple notifications', () => {
    spyOn(console, 'log');

    service.showSuccess('First message');
    service.showSuccess('Second message');

    expect(console.log).toHaveBeenCalledTimes(2);
    expect(console.log).toHaveBeenCalledWith('Success:', 'First message');
    expect(console.log).toHaveBeenCalledWith('Success:', 'Second message');
  });
});
