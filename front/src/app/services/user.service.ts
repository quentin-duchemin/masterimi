import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { IUser } from '../interfaces/user.interface';


@Injectable({ providedIn: 'root' })
export class UserService {

  constructor(private http: HttpClient) { }

  getCurrentUser(): Observable<IUser> {
    return this.http.get<IUser>('/users/me');
  }
}
