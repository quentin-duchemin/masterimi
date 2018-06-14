import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { IDepartment } from 'app/interfaces/department.interface';


@Injectable()
export class DepartmentsResolver implements Resolve<IDepartment[]> {
  constructor(
  ) {}

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<IDepartment[]> {
    return of([
      {
        id: 'IMI',
        name: 'Ingénierie Mathématique Informatique'
      },
    ]);
  }
}
