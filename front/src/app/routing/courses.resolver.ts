import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { ICourse } from 'app/interfaces/course.interface';
import { CourseService } from 'app/services/course.service';


@Injectable()
export class CoursesResolver implements Resolve<ICourse[]> {
  constructor(
    private readonly courseService: CourseService,
  ) {
  }

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<ICourse[]> {
    return this.courseService.getAll();
  }
}
