import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { ParcoursService } from 'app/services/parcours.service';


@Injectable()
export class ParcoursResolver implements Resolve<any> {
  constructor(
    private readonly parcoursService: ParcoursService,
  ) {
  }

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<any> {
    const id = +route.paramMap.get('id');
    return this.parcoursService.getOne(id);
  }
}
