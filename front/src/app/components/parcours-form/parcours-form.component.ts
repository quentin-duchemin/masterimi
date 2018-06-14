import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { IFormula } from 'app/interfaces/formula.interface';
import { IMaster } from 'app/interfaces/master.interface';
import { ICourse } from 'app/interfaces/course.interface';
import { IParcours } from 'app/interfaces/parcours.interface';
import { ParcoursService } from 'app/services/parcours.service';


@Component({
  selector: 'app-master-form',
  templateUrl: './parcours-form.component.html',
  styleUrls: ['./parcours-form.component.css'],
})
export class ParcoursFormComponent implements OnInit {
  form: FormGroup;
  disabled = false;

  masters: IMaster[];
  formulas: IFormula[];
  courses: ICourse[];

  constructor(
    private route: ActivatedRoute,
    private dialog: MatDialog,
    private fb: FormBuilder,
    private readonly parcoursService: ParcoursService,
  ) {
  }

  ngOnInit() {
    this.disabled = this.route.snapshot.data.view === 'show';

    this.masters = this.route.snapshot.data.masters;
    this.formulas = this.route.snapshot.data.formulas;
    this.courses = this.route.snapshot.data.courses;

    const parcours: IParcours = this.route.snapshot.data.parcours;

    this.form = this.fb.group({
      master: [parcours.master, Validators.required],
      formula: [parcours.formula, Validators.required],
      courses: [this.coursesIdToCourses(parcours.courses)],
      coursesOption2: [this.coursesIdToCourses(parcours.coursesOption2)],
    });

    if (this.disabled) {
      this.form.disable();
    }
  }

  get availableCourses() {
    const selectedCourses = [
      ...this.form.get('courses').value,
      ...this.form.get('coursesOption2').value,
    ];
    return this.courses.filter((course) => {
      return selectedCourses.find((selectedCourse) => selectedCourse.id === course.id) === undefined;
    });
  }

  submit() {
    const { master, formula, courses, coursesOption2 } = this.form.value;
    const parcours = {
      ...this.route.snapshot.data.parcours,
      master,
      formula,
      courses: courses.map((course) => course.id),
      coursesOption2: coursesOption2.map((course) => course.id),
    } as IParcours;

    this.parcoursService.update(parcours).subscribe(() => alert('wesh'));
  }

  coursesIdToCourses(coursesId) {
    return this.courses.filter((course) => coursesId.includes(course.id));
  }
}
