import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { UserFormComponent } from './user-form.component';
import { User } from '../../../core/services/auth.service';

describe('UserFormComponent', () => {
  let component: UserFormComponent;
  let fixture: ComponentFixture<UserFormComponent>;

  const mockUser: User = {
    id: '1',
    email: 'test@example.com',
    name: 'Test User',
    role: 'user'
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserFormComponent, ReactiveFormsModule, CommonModule]
    }).compileComponents();

    fixture = TestBed.createComponent(UserFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize form with empty values by default', () => {
    expect(component.userForm.get('name')?.value).toBe('');
    expect(component.userForm.get('email')?.value).toBe('');
    expect(component.userForm.get('role')?.value).toBe('user');
  });

  it('should initialize form with user values when user input is provided', () => {
    component.user = mockUser;
    component.ngOnInit();

    expect(component.userForm.get('name')?.value).toBe(mockUser.name);
    expect(component.userForm.get('email')?.value).toBe(mockUser.email);
    expect(component.userForm.get('role')?.value).toBe(mockUser.role);
  });

  it('should validate required fields', () => {
    const nameControl = component.userForm.get('name');
    const emailControl = component.userForm.get('email');

    nameControl?.setValue('');
    emailControl?.setValue('');

    expect(nameControl?.hasError('required')).toBe(true);
    expect(emailControl?.hasError('required')).toBe(true);
  });

  it('should validate email format', () => {
    const emailControl = component.userForm.get('email');

    emailControl?.setValue('invalid-email');
    expect(emailControl?.hasError('email')).toBe(true);

    emailControl?.setValue('valid@example.com');
    expect(emailControl?.hasError('email')).toBe(false);
  });

  it('should validate name minimum length', () => {
    const nameControl = component.userForm.get('name');

    nameControl?.setValue('a');
    expect(nameControl?.hasError('minlength')).toBe(true);

    nameControl?.setValue('ab');
    expect(nameControl?.hasError('minlength')).toBe(false);
  });

  it('should emit saveUser event on valid form submission', () => {
    spyOn(component.saveUser, 'emit');

    component.userForm.patchValue({
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin'
    });

    component.onSubmit();

    expect(component.saveUser.emit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin'
    });
  });

  it('should not emit saveUser event on invalid form submission', () => {
    spyOn(component.saveUser, 'emit');

    component.userForm.patchValue({
      name: '',
      email: 'invalid-email',
      role: 'user'
    });

    component.onSubmit();

    expect(component.saveUser.emit).not.toHaveBeenCalled();
  });

  it('should emit cancelEdit event', () => {
    spyOn(component.cancelEdit, 'emit');

    component.onCancel();

    expect(component.cancelEdit.emit).toHaveBeenCalled();
  });

  it('should return appropriate error messages', () => {
    const nameControl = component.userForm.get('name');
    const emailControl = component.userForm.get('email');

    nameControl?.setValue('');
    nameControl?.markAsTouched();
    expect(component.getFieldError('name')).toBe('name is required');

    nameControl?.setValue('a');
    nameControl?.markAsTouched();
    expect(component.getFieldError('name')).toBe('name must be at least 2 characters');

    emailControl?.setValue('invalid');
    emailControl?.markAsTouched();
    expect(component.getFieldError('email')).toBe('Please enter a valid email');
  });

  it('should return empty string for valid fields', () => {
    const nameControl = component.userForm.get('name');
    nameControl?.setValue('Valid Name');
    nameControl?.markAsTouched();

    expect(component.getFieldError('name')).toBe('');
  });

  it('should mark all controls as touched when invalid form is submitted', () => {
    component.userForm.patchValue({
      name: '',
      email: '',
      role: 'user'
    });

    component.onSubmit();

    expect(component.userForm.get('name')?.touched).toBe(true);
    expect(component.userForm.get('email')?.touched).toBe(true);
    expect(component.userForm.get('role')?.touched).toBe(true);
  });

  it('should handle loading state', () => {
    component.isLoading = true;
    expect(component.isLoading).toBe(true);

    component.isLoading = false;
    expect(component.isLoading).toBe(false);
  });

  it('should display form fields in template', () => {
    const compiled = fixture.nativeElement as HTMLElement;

    expect(compiled.querySelector('input[formControlName="name"]')).toBeTruthy();
    expect(compiled.querySelector('input[formControlName="email"]')).toBeTruthy();
    expect(compiled.querySelector('select[formControlName="role"]')).toBeTruthy();
  });

  it('should display save and cancel buttons', () => {
    const compiled = fixture.nativeElement as HTMLElement;
    const buttons = compiled.querySelectorAll('button');

    expect(buttons.length).toBe(2);
    expect(buttons[0].textContent?.trim()).toContain('Cancel');
    expect(buttons[1].textContent?.trim()).toContain('Save User');
  });
});
