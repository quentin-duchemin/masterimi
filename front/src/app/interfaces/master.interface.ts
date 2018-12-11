import { IOption } from "./option.interface";

export interface IMaster {
  id: string;
  name: string;
  shortName: string;
  availableOptions: IOption[];
}
