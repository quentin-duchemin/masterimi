import {
  MatAutocompleteModule,
  MatButtonModule,
  MatCardModule,
  MatCheckboxModule,
  MatChipsModule,
  MatDialogModule,
  MatDividerModule,
  MatFormFieldModule,
  MatIconModule,
  MatInputModule,
  MatListModule,
  MatProgressSpinnerModule,
  MatSelectModule,
  MatSidenavModule,
  MatSnackBarModule,
  MatTableModule,
  MatToolbarModule,
  MatTooltipModule,
  MatStepperModule,
} from '@angular/material';
import { NgModule } from '@angular/core';

const elementModules = [
  MatButtonModule,
  MatCheckboxModule,
  MatToolbarModule,
  MatFormFieldModule,
  MatTableModule,
  MatInputModule,
  MatSidenavModule,
  MatListModule,
  MatIconModule,
  MatTooltipModule,
  MatDividerModule,
  MatProgressSpinnerModule,
  MatDialogModule,
  MatCardModule,
  MatSnackBarModule,
  MatSelectModule,
  MatChipsModule,
  MatAutocompleteModule,
  MatStepperModule,
  MatProgressSpinnerModule,
];

@NgModule({
  imports: elementModules,
  exports: elementModules,
})
export class AppMaterialModule {}
