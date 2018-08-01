import { IMaster } from './master.interface';
import { ICourse } from './course.interface';

export interface IParcours {
  id: number;
  master: IMaster;
  option: string;
  user?: number;
  courseChoice: ICourseChoice;
}

export interface ICourseChoice {
  mainCourses: ICourse[];
  optionCourses: ICourse[];
  comment?: string;
  submitted: boolean;
}
