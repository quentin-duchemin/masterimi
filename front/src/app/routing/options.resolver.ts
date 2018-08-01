import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { IOption } from '../interfaces/option.interface';


@Injectable()
export class OptionsResolver implements Resolve<IOption[]> {
  constructor(
  ) {}

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<IOption[]> {
    return of([
      {
        id: '3A-ecole',
        name: '3A École',
      },
      {
        id: '3A-M2-PFE',
        name: '3A M2 Imbriqués - Option 1',
      },
      {
        id: '3A-M2-ECTS',
        name: '3A M2 Imbriqués - Option 2',
      },
    ]);
  }
}
