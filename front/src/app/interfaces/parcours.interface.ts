import { IMaster } from 'app/interfaces/master.interface';
import { ICourse } from 'app/interfaces/course.interface';

export interface IParcours {
  id?: number;
  master: IMaster;
  formula: string;
  user?: number;
  courses: ICourse[];
  coursesOption2: ICourse[];
}
