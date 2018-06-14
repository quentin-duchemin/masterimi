import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { IMaster } from 'app/interfaces/master.interface';


@Injectable({ providedIn: 'root' })
export class MasterService {

  constructor(private http: HttpClient) {
  }

  getAll(): Observable<IMaster[]> {
    return this.http.get<IMaster[]>('/masters');
  }
}
