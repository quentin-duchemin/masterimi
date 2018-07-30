import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MatDialog } from '@angular/material';
import { ConfirmDialogComponent } from './confirm/confirm-dialog.component';


@Injectable({ providedIn: 'root' })
export class DialogService {

    constructor(private readonly dialog: MatDialog) {}

    confirm(title: string, text: string): Observable<boolean> {
        const dialogRef = this.dialog.open(ConfirmDialogComponent, {
            width: '40vw',
            data: {
                title,
                text,
            },
        });

        return dialogRef.afterClosed();
    }
}
