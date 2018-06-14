import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { IParcours } from 'app/interfaces/parcours.interface';


@Injectable({ providedIn: 'root' })
export class ParcoursService {

  constructor(
    private readonly http: HttpClient,
  ) {
  }

  get(): Observable<IParcours> {
    return this.http.get<IParcours>('/users/me/parcours');
  }

  update(parcours: IParcours) {
    return this.http.put('/users/me/parcours', parcours);
  }
}
