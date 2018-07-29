import { Component, OnInit } from '@angular/core';

import { IParcours } from '../../interfaces/parcours.interface';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-parcours-intro',
  templateUrl: './parcours-intro.component.html',
  styleUrls: ['./parcours-intro.component.css']
})
export class ParcoursIntroComponent implements OnInit {
  parcours: IParcours;

  constructor(
    private authService: AuthService,
  ) {
  }

  ngOnInit() {
    this.authService.getCurrentUser().subscribe((currentUser) => {
      this.parcours = currentUser.parcours;
      console.log(this.parcours);
    });
  }

  get hasOption() {
    return !!this.parcours.option;
  }

  get hasNoCourses() {
    return !this.parcours.courseChoice;
  }

  get hasPendingCourses() {
    return !!this.parcours.courseChoice && !this.parcours.courseChoice.submitted;
  }

  get hasSubmittedCourses() {
    return !!this.parcours.courseChoice && this.parcours.courseChoice.submitted;
  }
}
