import { TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import { authGuard } from './auth.guard';
import { AuthService } from '../services/auth.service';

describe('authGuard', () => {
  let authServiceSpy: jasmine.SpyObj<AuthService>;
  let routerSpy: jasmine.SpyObj<Router>;
  let route: ActivatedRouteSnapshot;
  let state: RouterStateSnapshot;

  beforeEach(() => {
    const authSpy = jasmine.createSpyObj('AuthService', ['isAuthenticated']);
    const routerSpyObj = jasmine.createSpyObj('Router', ['navigate']);

    TestBed.configureTestingModule({
      providers: [
        { provide: AuthService, useValue: authSpy },
        { provide: Router, useValue: routerSpyObj },
      ],
    });

    authServiceSpy = TestBed.inject(AuthService) as jasmine.SpyObj<AuthService>;
    routerSpy = TestBed.inject(Router) as jasmine.SpyObj<Router>;

    route = {} as ActivatedRouteSnapshot;
    state = { url: '/protected-route' } as RouterStateSnapshot;
  });

  it('should allow access when user is authenticated', () => {
    authServiceSpy.isAuthenticated.and.returnValue(true);

    const result = TestBed.runInInjectionContext(() => authGuard(route, state));

    expect(result).toBe(true);
    expect(routerSpy.navigate).not.toHaveBeenCalled();
  });

  it('should redirect to login when user is not authenticated', () => {
    authServiceSpy.isAuthenticated.and.returnValue(false);

    const result = TestBed.runInInjectionContext(() => authGuard(route, state));

    expect(result).toBe(false);
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/login'], {
      queryParams: { returnUrl: '/protected-route' },
    });
  });

  it('should handle different URLs correctly', () => {
    const customState = { url: '/dashboard/settings' } as RouterStateSnapshot;
    authServiceSpy.isAuthenticated.and.returnValue(false);

    const result = TestBed.runInInjectionContext(() => authGuard(route, customState));

    expect(result).toBe(false);
    expect(routerSpy.navigate).toHaveBeenCalledWith(['/login'], {
      queryParams: { returnUrl: '/dashboard/settings' },
    });
  });
});
