import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog } from '@angular/material';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ICourse } from '../../interfaces/course.interface';
import { IParcours, ICourseChoice } from '../../interfaces/parcours.interface';
import { ParcoursService } from '../../services/parcours.service';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-master-form',
  templateUrl: './parcours-courses-form.component.html',
  styleUrls: ['./parcours-courses-form.component.css'],
})
export class ParcoursCoursesFormComponent implements OnInit {
  form: FormGroup;
  disabled = false;

  courses: ICourse[];

  parcours: IParcours;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly router: Router,
    private readonly dialog: MatDialog,
    private readonly fb: FormBuilder,
    private readonly authService: AuthService,
    private readonly parcoursService: ParcoursService,
  ) {
  }

  ngOnInit() {
    this.disabled = this.route.snapshot.data.view === 'show';

    this.courses = this.route.snapshot.data.courses;

    this.parcours = this.route.snapshot.data.parcours;

    const courseChoice: ICourseChoice = this.route.snapshot.data.parcours.courseChoice || {
      mainCourses: [],
      optionCourses: [],
    };

    this.form = this.fb.group({
      mainCourses: [this.coursesIdToCourses(courseChoice.mainCourses)],
      optionCourses: [this.coursesIdToCourses(courseChoice.optionCourses)],
      comment: [courseChoice.comment],
    });

    if (this.disabled) {
      this.form.disable();
    }
  }

  get availableCourses() {
    const selectedCourses = [
      ...this.form.get('mainCourses').value,
      ...this.form.get('optionCourses').value,
    ];
    return this.courses.filter((course) => {
      return selectedCourses.find((selectedCourse) => selectedCourse.id === course.id) === undefined;
    });
  }

  save() {
    this.performUpdate(false);
  }

  submit() {
    this.performUpdate(true);
  }

  private performUpdate(isSubmitted) {
    this.markAsTouched();

    const { mainCourses, optionCourses, comment } = this.form.value;
    const courseChoice = {
      mainCourses: mainCourses.map((course) => course.id),
      optionCourses: optionCourses.map((course) => course.id),
      comment,
      submitted: isSubmitted,
    } as ICourseChoice;

    this.parcoursService.updateCourseChoice(courseChoice).subscribe(() => {
      this.authService.reloadCurrentUser();
      this.router.navigateByUrl('/parcours');
    });
  }

  coursesIdToCourses(coursesId) {
    return this.courses.filter((course) => coursesId.includes(course.id));
  }

  private markAsTouched() {
    Object.values(this.form.controls).forEach(control => control.markAsTouched());
  }
}
