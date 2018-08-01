import { Component, OnInit } from '@angular/core';

import { IParcours } from '../../interfaces/parcours.interface';
import { AuthService } from '../../services/auth.service';
import { ActivatedRoute } from '@angular/router';
import { IOption } from '../../interfaces/option.interface';
import { ParcoursService } from '../../services/parcours.service';
import { DialogService } from '../../services/dialog/dialog.service';


@Component({
  selector: 'app-parcours-intro',
  templateUrl: './parcours-intro.component.html',
  styleUrls: ['./parcours-intro.component.css']
})
export class ParcoursIntroComponent implements OnInit {
  options: IOption[];

  parcours: IParcours;
  selectedOption: IOption;

  constructor(
    private readonly route: ActivatedRoute,
    private readonly authService: AuthService,
    private readonly dialogService: DialogService,
    private readonly parcoursService: ParcoursService,
  ) {
  }

  ngOnInit() {
    this.options = this.route.snapshot.data.options;

    this.authService.getCurrentUser().subscribe((currentUser) => {
      this.parcours = currentUser.parcours;
    });
  }

  get hasOption() {
    return !!this.parcours.option;
  }

  get displayOption() {
    const option = this.options.find((option) => option.id === this.parcours.option);

    if (!option) {
      return this.parcours.option;
    }

    return option.name;
  }

  submitOption() {
    if (!this.selectedOption) {
      return;
    }

    this.dialogService.confirm(
      'Confirmation',
      `Es-tu certain de vouloir choisir l\'option ${this.selectedOption.name} ?`,
    ).subscribe((confirmed) => {
      if (!confirmed) {
        return;
      }

      this.parcoursService.updateOption(this.selectedOption).subscribe(() => {
        this.authService.reloadCurrentUser();
      });
    })
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
