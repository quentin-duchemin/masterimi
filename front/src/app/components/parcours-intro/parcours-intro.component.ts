import { Component, OnInit } from '@angular/core';

import { IParcours } from 'app/interfaces/parcours.interface';
import { AuthService } from 'app/services/auth.service';


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
    });
  }

  get hasNoParcours() {
    return !this.parcours;
  }

  get hasPendingParcours() {
    return !!this.parcours && !this.parcours.submitted;
  }

  get hasSubmittedParcours() {
    return !!this.parcours && this.parcours.submitted;
  }
}
