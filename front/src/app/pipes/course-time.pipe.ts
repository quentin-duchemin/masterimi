import { Pipe, PipeTransform } from '@angular/core';

@Pipe({ name: 'courseTime' })
export class CourseTimePipe implements PipeTransform {
    transform(value: string): string {
        if (!value) {
            return '';
        }

        const [day, start, end] = value.split('/');

        return `${this.toFR(day)} de ${start} à ${end}`;
    }

    private toFR(day: string) {
        switch (day) {
            case 'Mon':
                return 'Lundi';
            case 'Tue':
                return 'Mardi';
            case 'Wed':
                return 'Mercredi';
            case 'Thu':
                return 'Jeudi';
            case 'Fri':
                return 'Vendredi';
            default:
                return NaN;
        }
    }
}
