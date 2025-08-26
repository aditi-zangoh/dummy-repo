import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  showSuccess(message: string): void {
    // Implementation for success notification
    console.log('Success:', message);
  }

  showError(message: string): void {
    // Implementation for error notification
    console.error('Error:', message);
  }

  showWarning(message: string): void {
    // Implementation for warning notification
    console.warn('Warning:', message);
  }
}
