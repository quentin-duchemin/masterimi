import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { IUser } from '../../interfaces/user.interface';

@Component({
  selector: 'app-layout',
  templateUrl: './layout.component.html',
  styleUrls: ['./layout.component.css']
})
export class LayoutComponent implements OnInit {
  currentUser: IUser;

  sideNavOpened = true;

  constructor(
    private readonly authService: AuthService,
  ) {
  }

  ngOnInit() {
    this.authService.reloadCurrentUser();

    this.authService.getCurrentUser().subscribe((currentUser) => {
      this.currentUser = currentUser;
    });
  }

  logout() {
    this.authService.logout();
  }

  toggleSidenav() {
    this.sideNavOpened = !this.sideNavOpened;
  }
}
