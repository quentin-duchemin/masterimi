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
  MatSortModule,
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
  MatSortModule,
];

@NgModule({
  imports: elementModules,
  exports: elementModules,
})
export class AppMaterialModule {}
