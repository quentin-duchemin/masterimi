import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ICourse } from 'app/interfaces/course.interface';
import { IParcours, ICourseChoice } from 'app/interfaces/parcours.interface';
import { ParcoursService } from 'app/services/parcours.service';
import { AuthService } from 'app/services/auth.service';
import { IValidationData } from 'app/interfaces/validation-data.interface';
import { DialogService } from 'app/services/dialog/dialog.service';


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
    private readonly fb: FormBuilder,
    private readonly authService: AuthService,
    private readonly dialogService: DialogService,
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
    if (this.parcours.option.id == '3A-ecole') {
      return this.availableCourses;
    }

    return this.availableCourses.filter((course) => course.masters.includes(this.parcours.master.id));
  }

  save() {
    this.performUpdate(false);
  }

  submit() {
    this.dialogService.confirm(
      'Confirmation',
      'Es-tu certain de vouloir envoyer tes choix de cours de 3A ?',
    ).subscribe((confirmed) => {
      if (!confirmed) {
        return;
      }

      this.performUpdate(true);
    });
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
    if (ruleType == 'error') {
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
