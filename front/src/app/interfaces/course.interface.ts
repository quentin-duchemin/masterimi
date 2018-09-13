import { IMaster } from "app/interfaces/master.interface";

export interface ICourse {
  id: number;
  name: string;
  ECTS: string;
  period: string;
  location: string;
  time: string;
  master: IMaster;
}
