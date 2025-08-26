import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { FormInputComponent } from './components/form-input/form-input.component';
import { ButtonComponent } from './components/button/button.component';
import { CapitalizePipe } from './pipes/capitalize.pipe';

@NgModule({
  declarations: [CapitalizePipe],
  imports: [CommonModule, FormsModule, ReactiveFormsModule, FormInputComponent, ButtonComponent],
  exports: [CommonModule, FormsModule, ReactiveFormsModule, FormInputComponent, ButtonComponent, CapitalizePipe],
})
export class SharedModule {}
