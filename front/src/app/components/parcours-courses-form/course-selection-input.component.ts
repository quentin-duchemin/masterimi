import { Component, forwardRef, Input, OnInit } from '@angular/core';
import { MatDialog, MatTableDataSource } from '@angular/material';
import { CourseSelectionDialogComponent } from './course-selection-dialog.component';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { ICourse } from '../../interfaces/course.interface';


@Component({
  selector: 'app-course-selection-input',
  templateUrl: './course-selection-input.component.html',
  styleUrls: ['./course-selection-input.component.css'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      multi: true,
      useExisting: forwardRef(() => CourseSelectionInputComponent),
    }
  ]
})
export class CourseSelectionInputComponent implements OnInit, ControlValueAccessor {
  dataSource: MatTableDataSource<any>;

  isDisabled = false;
  onChange = (newValue?) => {};

  @Input()
  availableCourses: any[];

  @Input()
  mode: string;

  constructor(
    private dialog: MatDialog,
  ) {}

  ngOnInit() {
    this.dataSource = new MatTableDataSource([]);
  }

  get displayedColumns() {
    const baseColumns = ['name', 'master', 'location', 'ECTS'];

    if (this.isDisabled) {
      return baseColumns;
    }

    return [
      ...baseColumns,
      'actions',
    ];
  }


  get selectedCourses() {
    return this.dataSource.data;
  }

  set selectedCourses(selectedCourses: any[]) {
    this.dataSource.data = selectedCourses;
    this.onChange(this.selectedCourses);
  }

  remove(element) {
    this.selectedCourses = this.selectedCourses.filter((x) => x.id !== element.id);
  }

  openCourseSelectionDialog() {
    const dialogRef = this.dialog.open(CourseSelectionDialogComponent, {
      width: '65vw',
      data: {
        availableCourses: this.availableCourses,
      },
    });

    dialogRef.afterClosed().subscribe((selectedCourses) => {
      if (selectedCourses) {
        this.selectedCourses = [
          ...this.selectedCourses,
          ...selectedCourses,
        ];
      }
    });
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
  }

  setDisabledState(isDisabled: boolean): void {
    this.isDisabled = isDisabled;
  }

  writeValue(obj: any): void {
    this.dataSource.data = obj;
  }

  formatECTSSum(): string {
    switch (this.mode) {
      case '3A':
        return `Total d'ECTS pour la 3A : ${this.computeECTSSum()} / 30`;
      case 'option2':
        return `Total d'ECTS pour l'option 2 : ${this.computeECTSSum()} / 15`;
      default:
        return '';
    }
  }

  getECTSSumClass()  {
    if (this.mode === '3A' && this.computeECTSSum() < 30) {
      return 'ECTS-wrapper ECTS-error';
    }

    if (this.mode === 'option2' && this.computeECTSSum() < 15) {
      return 'ECTS-wrapper ECTS-error';
    }

    return 'ECTS-wrapper';
  }

  computeECTSSum(): number {
    return this.selectedCourses.reduce((agg: number, item: ICourse) => agg + item.ECTS, 0);
  }
}
