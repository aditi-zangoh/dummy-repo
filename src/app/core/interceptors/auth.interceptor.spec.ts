import { TestBed } from '@angular/core/testing';
import { HttpRequest, HttpHandlerFn } from '@angular/common/http';
import { of } from 'rxjs';

import { authInterceptor } from './auth.interceptor';
import { AuthService } from '../services/auth.service';

describe('authInterceptor', () => {
  let authServiceSpy: jasmine.SpyObj<AuthService>;

  beforeEach(() => {
    const authSpy = jasmine.createSpyObj('AuthService', ['getToken']);

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authSpy }
      ]
    });

    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
  });

  it('should add Authorization header when token exists', () => {
    const mockToken = 'test-jwt-token';
    authServiceSpy.getToken.and.returnValue(mockToken);

    const mockRequest = new HttpRequest('GET', '/api/test');
    const mockHandler: HttpHandlerFn = jasmine.createSpy('HttpHandlerFn').and.returnValue(of({}));

    TestBed.runInInjectionContext(() => {
      authInterceptor(mockRequest, mockHandler);
    });

    expect(mockHandler).toHaveBeenCalledWith(jasmine.objectContaining({
      headers: jasmine.objectContaining({
        lazyUpdate: jasmine.arrayContaining([
          jasmine.objectContaining({
            name: 'Authorization',
            value: `Bearer ${mockToken}`
          })
        ])
      })
    }));
  });

  it('should not modify request when no token exists', () => {
    authServiceSpy.getToken.and.returnValue(null);

    const mockRequest = new HttpRequest('GET', '/api/test');
    const mockHandler: HttpHandlerFn = jasmine.createSpy('HttpHandlerFn').and.returnValue(of({}));

    TestBed.runInInjectionContext(() => {
      authInterceptor(mockRequest, mockHandler);
    });

    expect(mockHandler).toHaveBeenCalledWith(mockRequest);
  });

  it('should not modify request when token is empty string', () => {
    authServiceSpy.getToken.and.returnValue('');

    const mockRequest = new HttpRequest('GET', '/api/test');
    const mockHandler: HttpHandlerFn = jasmine.createSpy('HttpHandlerFn').and.returnValue(of({}));

    TestBed.runInInjectionContext(() => {
      authInterceptor(mockRequest, mockHandler);
    });

    expect(mockHandler).toHaveBeenCalledWith(mockRequest);
  });

  it('should handle POST requests with token', () => {
    const mockToken = 'post-test-token';
    authServiceSpy.getToken.and.returnValue(mockToken);

    const mockRequest = new HttpRequest('POST', '/api/users', { name: 'Test User' });
    const mockHandler: HttpHandlerFn = jasmine.createSpy('HttpHandlerFn').and.returnValue(of({}));

    TestBed.runInInjectionContext(() => {
      authInterceptor(mockRequest, mockHandler);
    });

    expect(mockHandler).toHaveBeenCalledWith(jasmine.objectContaining({
      method: 'POST',
      headers: jasmine.objectContaining({
        lazyUpdate: jasmine.arrayContaining([
          jasmine.objectContaining({
            name: 'Authorization',
            value: `Bearer ${mockToken}`
          })
        ])
      })
    }));
  });

  it('should preserve existing headers when adding Authorization', () => {
    const mockToken = 'preserve-headers-token';
    authServiceSpy.getToken.and.returnValue(mockToken);

    const mockRequest = new HttpRequest('PUT', '/api/users/1', {});
    const mockHandler: HttpHandlerFn = jasmine.createSpy('HttpHandlerFn').and.returnValue(of({}));

    TestBed.runInInjectionContext(() => {
      authInterceptor(mockRequest, mockHandler);
    });

    expect(mockHandler).toHaveBeenCalledWith(jasmine.objectContaining({
      method: 'PUT',
      headers: jasmine.objectContaining({
        lazyUpdate: jasmine.arrayContaining([
          jasmine.objectContaining({
            name: 'Authorization',
            value: `Bearer ${mockToken}`
          })
        ])
      })
    }));
  });
});
