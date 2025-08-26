import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { HttpParams } from '@angular/common/http';

import { ApiService, ApiResponse } from './api.service';

describe('ApiService', () => {
  let service: ApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    service = TestBed.inject(ApiService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('GET requests', () => {
    it('should make successful GET request', () => {
      const mockResponse: ApiResponse<{id: number; name: string}> = {
        data: { id: 1, name: 'Test' },
        message: 'Success',
        success: true,
      };

      service.get<{id: number; name: string}>('test-endpoint').subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('https://api.example.com/test-endpoint');
      expect(req.request.method).toBe('GET');
      expect(req.request.headers.get('Content-Type')).toBe('application/json');
      expect(req.request.headers.get('Accept')).toBe('application/json');
      req.flush(mockResponse);
    });

    it('should make GET request with params', () => {
      const params = new HttpParams().set('page', '1').set('limit', '10');
      const mockResponse: ApiResponse<unknown[]> = {
        data: [],
        message: 'Success',
        success: true,
      };

      service.get<unknown[]>('users', params).subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('https://api.example.com/users?page=1&limit=10');
      expect(req.request.method).toBe('GET');
      req.flush(mockResponse);
    });

    it('should retry GET request twice on failure then succeed', () => {
      const mockResponse: ApiResponse<{id: number}> = {
        data: { id: 1 },
        message: 'Success',
        success: true,
      };

      service.get<{id: number}>('retry-test').subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      // First two requests should fail
      for (let i = 0; i < 2; i++) {
        const req = httpMock.expectOne('https://api.example.com/retry-test');
        req.flush('Error', { status: 500, statusText: 'Internal Server Error' });
      }

      // Third request should succeed
      const req = httpMock.expectOne('https://api.example.com/retry-test');
      req.flush(mockResponse);
    });
  });

  describe('POST requests', () => {
    it('should make successful POST request', () => {
      const postData = { name: 'Test User', email: 'test@example.com' };
      const mockResponse: ApiResponse<{id: number; name: string; email: string}> = {
        data: { id: 1, ...postData },
        message: 'Created successfully',
        success: true,
      };

      service.post<{id: number; name: string; email: string}>('users', postData).subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('https://api.example.com/users');
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual(postData);
      req.flush(mockResponse);
    });
  });

  describe('PUT requests', () => {
    it('should make successful PUT request', () => {
      const putData = { id: 1, name: 'Updated User' };
      const mockResponse: ApiResponse<{id: number; name: string}> = {
        data: putData,
        message: 'Updated successfully',
        success: true,
      };

      service.put<{id: number; name: string}>('users/1', putData).subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('https://api.example.com/users/1');
      expect(req.request.method).toBe('PUT');
      expect(req.request.body).toEqual(putData);
      req.flush(mockResponse);
    });
  });

  describe('DELETE requests', () => {
    it('should make successful DELETE request', () => {
      const mockResponse: ApiResponse<null> = {
        data: null,
        message: 'Deleted successfully',
        success: true,
      };

      service.delete<null>('users/1').subscribe((response) => {
        expect(response).toEqual(mockResponse);
      });

      const req = httpMock.expectOne('https://api.example.com/users/1');
      expect(req.request.method).toBe('DELETE');
      req.flush(mockResponse);
    });
  });

  describe('Error handling', () => {
    it('should handle client-side errors', () => {
      const errorEvent = new ErrorEvent('Network error', {
        message: 'Connection failed',
      });

      service.get<unknown>('error-test').subscribe({
        next: () => fail('Expected an error'),
        error: (error) => {
          expect(error.message).toContain('Client Error: Connection failed');
        },
      });

      const req = httpMock.expectOne('https://api.example.com/error-test');
      req.error(errorEvent);
    });

    it('should handle server-side errors', () => {
      service.get<unknown>('server-error-test').subscribe({
        next: () => fail('Expected an error'),
        error: (error) => {
          expect(error.message).toContain('Server Error: 404');
        },
      });

      const req = httpMock.expectOne('https://api.example.com/server-error-test');
      req.flush('Not Found', { status: 404, statusText: 'Not Found' });
    });
  });
});
