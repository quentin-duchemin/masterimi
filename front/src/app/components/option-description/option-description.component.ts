import { Component, Input } from '@angular/core';
import { IOption } from '../../interfaces/option.interface';

@Component({
  selector: 'app-option-description',
  templateUrl: './option-description.component.html',
  styleUrls: ['./option-description.component.css']
})
export class OptionDescriptionComponent {
  @Input()
  options: IOption[];

  inOptions(optionId: string) {
    if(this.options === undefined) {
      return true;
    }

    return this.options.find(option => option.id == optionId);
  }
}
