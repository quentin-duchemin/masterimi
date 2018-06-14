import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { IFormula } from 'app/interfaces/formula.interface';


@Injectable()
export class FormulasResolver implements Resolve<IFormula[]> {
  constructor(
  ) {}

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<IFormula[]> {
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
