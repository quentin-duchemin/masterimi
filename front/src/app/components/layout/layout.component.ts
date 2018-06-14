import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import {IUser} from '../../interfaces/user.interface';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.css']
})
export class LayoutComponent implements OnInit {
  currentUser: IUser;

  sideNavOpened = true;

  constructor(
      private readonly route: ActivatedRoute,
      private readonly authService: AuthService,
  ) { }

  ngOnInit() {
    this.currentUser = this.route.snapshot.data.currentUser;
  }

  logout() {
    this.authService.logout();
  }

  toggleSidenav() {
    this.sideNavOpened = !this.sideNavOpened;
  }
}
