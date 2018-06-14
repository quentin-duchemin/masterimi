import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { IMaster } from 'app/interfaces/master.interface';
import { MasterService } from 'app/services/master.service';


@Injectable()
export class MastersResolver implements Resolve<IMaster[]> {
  constructor(
    private readonly masterService: MasterService,
  ) {
  }

  resolve(route: ActivatedRouteSnapshot,
          state: RouterStateSnapshot): Observable<IMaster[]> {
    return this.masterService.getAll();
  }
}


