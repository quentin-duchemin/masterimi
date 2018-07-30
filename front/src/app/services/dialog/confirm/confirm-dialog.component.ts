import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material';

@Component({
    templateUrl: './confirm-dialog.component.html',
})
export class ConfirmDialogComponent {
    title: string;
    text: string;

    constructor(
        private dialogRef: MatDialogRef<ConfirmDialogComponent>,
        @Inject(MAT_DIALOG_DATA) data,
    ) {
        this.title = data.title;
        this.text = data.text;
    }
}
