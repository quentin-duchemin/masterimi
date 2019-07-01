import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { IUser } from '../interfaces/user.interface';
import { UserService } from './user.service';
import { environment } from 'environments/environment';
import { BehaviorSubject, Observable } from 'rxjs';

import * as Cookies from 'js-cookie';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser = new BehaviorSubject<IUser>({} as IUser);

  constructor(
    private readonly router: Router,
    private readonly userService: UserService,
  ) {
  }

  casLogin() {
    if (this.isLoggedIn()) {
      return this.router.navigateByUrl('/');
    }

    this.userService.getCurrentUser().subscribe(
      (currentUser) => {
        this.currentUser.next(currentUser);
        this.router.navigateByUrl('/');
      },
      (error) => {
        window.location.href = environment.casUrl;
      }
    );
  }

  logout() {
    this.cleanStorage();
    this.router.navigateByUrl('/login');
  }

  reloadCurrentUser() {
    this.userService.getCurrentUser().subscribe((currentUser) => {
      this.currentUser.next(currentUser);
    });
  }

  private cleanStorage(): void {
    this.currentUser.next({} as IUser);
  }

  isLoggedIn(): boolean {
    // FIXME this is hacky but sessionid cookies are only avaible with HTTPS
    const cookie = Cookies.get(environment.production ? 'sessionid' : 'csrftoken');
    return cookie != null;
  }

  getCurrentUser(): Observable<IUser> {
    return this.currentUser.asObservable();
  }
}
