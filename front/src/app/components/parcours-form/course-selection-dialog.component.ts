import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-course-selection-dialog',
  templateUrl: 'course-selection-dialog.component.html',
  styleUrls: ['./course-selection-dialog.component.css'],
})
export class CourseSelectionDialogComponent implements OnInit {
  @ViewChild('courses')
  courses;

  dataSource: MatTableDataSource<any>;

  constructor(
    public dialogRef: MatDialogRef<CourseSelectionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any,
  ) {}

  ngOnInit(): void {
    this.dataSource = new MatTableDataSource(this.data.availableCourses);
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim(); // Remove whitespace
    filterValue = filterValue.toLowerCase(); // MatTableDataSource defaults to lowercase matches
    this.dataSource.filter = filterValue;
  }

  handleSubmit() {
    const selectedCourses = this.courses.selectedOptions.selected.map((option) => option.value);

    return this.dialogRef.close(selectedCourses);
  }
}
