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
  option2Courses: ICourse[];
  comment?: string;
  submitted: boolean;
}
