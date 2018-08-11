import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { IUser } from '../interfaces/user.interface';
import { UserService } from './user.service';
import { environment } from 'environments/environment';
import { BehaviorSubject, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

const STORAGE_KEY = 'master_imi_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser = new BehaviorSubject<IUser>({} as IUser);
  private accessToken: string;

  constructor(
    private readonly router: Router,
    private readonly userService: UserService,
  ) {
    const savedToken = localStorage.getItem(STORAGE_KEY);

    this.loadToken(savedToken);
  }

  casLogin() {
    if (this.isLoggedIn()) {
      return this.router.navigateByUrl('/');
    }

    this.userService.getCurrentUser().subscribe(
      (currentUser) => {
        this.loadToken('DUMMY_TOKEN');
        this.currentUser.next(currentUser);
        this.router.navigateByUrl('/');
      },
      (error) => {
        window.location.href = environment.casUrl;
      }
    );
  }

  login(username: string, password: string): Observable<string> {
    return this.userService.login(username, password).pipe(
      tap(accessToken => this.loadToken(accessToken)),
    );
  }

  logout() {
    this.cleanStorage();
    this.router.navigateByUrl('/login');
  }

  private loadToken(accessToken: string): void {
    if (accessToken == null) {
      return;
    }

    localStorage.setItem(STORAGE_KEY, accessToken);
    this.accessToken = accessToken;
  }

  reloadCurrentUser() {
    this.userService.getCurrentUser().subscribe((currentUser) => {
      this.currentUser.next(currentUser);
    });
  }

  private cleanStorage(): void {
    localStorage.removeItem(STORAGE_KEY);
    this.accessToken = null;
    this.currentUser.next({} as IUser);
  }

  isLoggedIn(): boolean {
    return this.accessToken != null;
  }

  getAccessToken(): string {
    return this.accessToken;
  }

  getCurrentUser(): Observable<IUser> {
    return this.currentUser.asObservable();
  }
}
