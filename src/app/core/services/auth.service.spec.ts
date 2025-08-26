import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';

import { AuthService, User, LoginCredentials } from './auth.service';
import { ApiService, ApiResponse } from './api.service';

describe('AuthService', () => {
  let service: AuthService;
  let apiServiceSpy: jasmine.SpyObj<ApiService>;
  let localStorageSpy: jasmine.SpyObj<Storage>;

  const mockUser: User = {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user',
  };

  beforeEach(() => {
    const apiSpy = jasmine.createSpyObj('ApiService', ['post', 'get']);
    localStorageSpy = jasmine.createSpyObj('localStorage', ['getItem', 'setItem', 'removeItem', 'clear', 'key']);

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [{ provide: ApiService, useValue: apiSpy }],
    });

    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: localStorageSpy,
      writable: true,
    });

    service = TestBed.inject(AuthService);
    apiServiceSpy = TestBed.inject(ApiService) as jasmine.SpyObj<ApiService>;
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('initialization', () => {
    it('should load current user if token exists', () => {
      const mockResponse: ApiResponse<User> = {
        data: mockUser,
        message: 'Success',
        success: true,
      };

      localStorageSpy.getItem.and.returnValue('valid-token');
      apiServiceSpy.get.and.returnValue(of(mockResponse));

      service = TestBed.inject(AuthService);

      expect(localStorageSpy.getItem).toHaveBeenCalledWith('auth_token');
      expect(apiServiceSpy.get).toHaveBeenCalledWith('auth/me');
      expect(service.getCurrentUser()).toEqual(mockUser);
    });

    it('should not load user if no token exists', () => {
      localStorageSpy.getItem.and.returnValue(null);

      service = TestBed.inject(AuthService);

      expect(localStorageSpy.getItem).toHaveBeenCalledWith('auth_token');
      expect(apiServiceSpy.get).not.toHaveBeenCalled();
      expect(service.getCurrentUser()).toBeNull();
    });

    it('should logout if user loading fails', () => {
      localStorageSpy.getItem.and.returnValue('invalid-token');
      apiServiceSpy.get.and.returnValue(throwError(() => new Error('Unauthorized')));

      spyOn(service, 'logout');
      service = TestBed.inject(AuthService);

      expect(apiServiceSpy.get).toHaveBeenCalledWith('auth/me');
      expect(service.logout).toHaveBeenCalled();
    });
  });

  describe('login', () => {
    it('should call API login endpoint', () => {
      const credentials: LoginCredentials = {
        email: 'test@example.com',
        password: 'password123',
      };
      const mockResponse: ApiResponse<{ token: string }> = {
        data: { token: 'login-token' },
        message: 'Login successful',
        success: true,
      };

      apiServiceSpy.post.and.returnValue(of(mockResponse));

      service.login(credentials).subscribe(response => {
        expect(response).toEqual(mockResponse);
      });

      expect(apiServiceSpy.post).toHaveBeenCalledWith('auth/login', credentials);
    });
  });

  describe('logout', () => {
    it('should remove token and clear current user', () => {
      // Set up initial state with user logged in
      service['currentUserSubject'].next(mockUser);

      service.logout();

      expect(localStorageSpy.removeItem).toHaveBeenCalledWith('auth_token');
      expect(service.getCurrentUser()).toBeNull();
    });
  });

  describe('token management', () => {
    it('should set token in localStorage', () => {
      const token = 'test-token';

      service.setToken(token);

      expect(localStorageSpy.setItem).toHaveBeenCalledWith('auth_token', token);
    });

    it('should get token from localStorage', () => {
      const token = 'stored-token';
      localStorageSpy.getItem.and.returnValue(token);

      const result = service.getToken();

      expect(localStorageSpy.getItem).toHaveBeenCalledWith('auth_token');
      expect(result).toBe(token);
    });

    it('should return null when no token exists', () => {
      localStorageSpy.getItem.and.returnValue(null);

      const result = service.getToken();

      expect(result).toBeNull();
    });
  });

  describe('authentication status', () => {
    it('should return true when token exists', () => {
      localStorageSpy.getItem.and.returnValue('valid-token');

      const isAuth = service.isAuthenticated();

      expect(isAuth).toBe(true);
    });

    it('should return false when no token exists', () => {
      localStorageSpy.getItem.and.returnValue(null);

      const isAuth = service.isAuthenticated();

      expect(isAuth).toBe(false);
    });

    it('should return false when token is empty string', () => {
      localStorageSpy.getItem.and.returnValue('');

      const isAuth = service.isAuthenticated();

      expect(isAuth).toBe(false);
    });
  });

  describe('current user management', () => {
    it('should return current user', () => {
      service['currentUserSubject'].next(mockUser);

      const currentUser = service.getCurrentUser();

      expect(currentUser).toEqual(mockUser);
    });

    it('should emit user changes through observable', done => {
      service.currentUser$.subscribe(user => {
        if (user) {
          expect(user).toEqual(mockUser);
          done();
        }
      });

      service['currentUserSubject'].next(mockUser);
    });
  });
});
