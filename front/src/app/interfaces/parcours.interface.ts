import { IMaster } from './master.interface';
import { ICourse } from './course.interface';
import { IOption } from './option.interface';

export interface IParcours {
  id: number;
  master: IMaster;
  option: IOption;
  user?: number;
  courseChoice: ICourseChoice;
}

export interface ICourseChoice {
  mainCourses: ICourse[];
  optionCourses: ICourse[];
  comment?: string;
  submitted: boolean;
}
