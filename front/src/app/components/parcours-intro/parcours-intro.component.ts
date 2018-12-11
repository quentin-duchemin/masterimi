import { Component, OnInit } from '@angular/core';

import { IParcours } from '../../interfaces/parcours.interface';
import { AuthService } from '../../services/auth.service';
import { IOption } from '../../interfaces/option.interface';
import { ParcoursService } from '../../services/parcours.service';
import { DialogService } from '../../services/dialog/dialog.service';


@Component({
  selector: 'app-parcours-intro',
  templateUrl: './parcours-intro.component.html',
  styleUrls: ['./parcours-intro.component.css']
})
export class ParcoursIntroComponent implements OnInit {
  availableOptions: IOption[];

  parcours: IParcours;
  selectedOption: IOption;

  constructor(
    private readonly authService: AuthService,
    private readonly dialogService: DialogService,
    private readonly parcoursService: ParcoursService,
  ) {
  }

  ngOnInit() {
    this.authService.getCurrentUser().subscribe((currentUser) => {
      this.parcours = currentUser.parcours;
      if (this.parcours && this.parcours.master) {
        this.availableOptions = this.parcours.master.availableOptions;
      }
    });
  }

  get hasOption() {
    return !!this.parcours.option;
  }

  get displayOption() {
    return this.parcours.option.name;
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
