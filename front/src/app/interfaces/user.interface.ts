import { IParcours } from './parcours.interface';

export interface IUser {
  id: number;
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  parcours: IParcours;
}
