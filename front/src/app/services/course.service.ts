import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { ICourse } from '../interfaces/course.interface';


@Injectable({ providedIn: 'root' })
export class CourseService {

  constructor(private http: HttpClient) {
  }

  getAll(): Observable<ICourse[]> {
    return this.http.get<ICourse[]>('/courses');
  }
}
