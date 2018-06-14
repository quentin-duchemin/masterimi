import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { ParcoursService } from 'app/services/parcours.service';
import { IParcours } from 'app/interfaces/parcours.interface';


@Injectable()
export class ParcoursResolver implements Resolve<IParcours> {
  constructor(
    private readonly parcoursService: ParcoursService,
  ) {
  }

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<IParcours> {
    return this.parcoursService.get();
  }
}
