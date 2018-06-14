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

  getOne(id: number): Observable<IParcours> {
    return this.http.get<IParcours>(`/parcours/${id}`);
  }

  update(parcours: IParcours) {
    return this.http.put(`/parcours/${parcours.id}`, parcours);
  }
}
