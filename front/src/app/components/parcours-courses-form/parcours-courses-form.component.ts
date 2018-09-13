import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatDialog } from '@angular/material';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ICourse } from '../../interfaces/course.interface';
import { IParcours, ICourseChoice } from '../../interfaces/parcours.interface';
import { ParcoursService } from '../../services/parcours.service';
import { AuthService } from '../../services/auth.service';
import { IValidationData } from '../../interfaces/validation-data.interface';


@Component({
  selector: 'app-master-form',
  templateUrl: './parcours-courses-form.component.html',
  styleUrls: ['./parcours-courses-form.component.css'],
})
export class ParcoursCoursesFormComponent implements OnInit {
  form: FormGroup;
  disabled = false;

  courses: ICourse[];
  checkParcoursRules: IValidationData[] = [];

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

    this.form.valueChanges.subscribe(this.checkParcours);
    this.checkParcours(this.form.value);

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

  get availableMasterCourses() {
    return this.availableCourses
      .filter((course) => course.master ? course.master.id === this.parcours.master.id : false)
    ;
  }

  save() {
    this.performUpdate(false);
  }

  submit() {
    this.performUpdate(true);
  }

  private performUpdate(isSubmitted) {
    this.markAsTouched();

    const courseChoice = buildCourseChoice(this.form.value, isSubmitted);

    this.parcoursService.updateCourseChoice(courseChoice).subscribe(() => {
      this.authService.reloadCurrentUser();
      this.router.navigateByUrl('/parcours');
    });
  }

  coursesIdToCourses(coursesId) {
    return this.courses.filter((course) => coursesId.includes(course.id));
  }

  ruleTypeToIcon(ruleType: string) {
    if (ruleType == 'invalid') {
      return 'close';
    }

    if (ruleType == 'warning') {
      return 'warning';
    }

    if (ruleType == 'valid') {
      return 'check';
    }

    return '';
  }

  private markAsTouched() {
    Object.values(this.form.controls).forEach(control => control.markAsTouched());
  }

  private checkParcours = (form) => {
    const courseChoice = buildCourseChoice(form, false);

    this.parcoursService.checkCourseChoice(courseChoice).subscribe((res) => {
      this.checkParcoursRules = res;
    });
  }
}

function buildCourseChoice(formValue, isSubmitted: boolean): ICourseChoice {
  const { mainCourses, optionCourses, comment } = formValue;
  const courseChoice = {
    mainCourses: mainCourses.map((course) => course.id),
    optionCourses: optionCourses.map((course) => course.id),
    comment,
    submitted: isSubmitted,
  } as ICourseChoice;

  return courseChoice;
}
