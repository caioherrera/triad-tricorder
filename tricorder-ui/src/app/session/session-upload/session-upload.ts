import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Session, SessionService } from '../../../services/session-service';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatGridListModule } from '@angular/material/grid-list';
import { CommonModule, Location } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatListModule } from '@angular/material/list';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { Workload, WorkloadService } from '../../../services/workload-service';
import { map, Observable, startWith } from 'rxjs';

@Component({
  selector: 'session-upload',
  imports: [ CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule,
    MatCheckboxModule, MatAutocompleteModule, ReactiveFormsModule, MatSelectModule, MatListModule ],
  templateUrl: './session-upload.html',
  styleUrls: ['../../../styles.scss', './session-upload.scss']
})
export class SessionUploadComponent { 

    private _snackBar = inject(MatSnackBar);
    private readonly _router = inject(Router);
    
    session: Session = new Session();
    currFileNames: string = '';

    workloads: Workload[] = [];
    selectedWorkload: string = "";
    workloadAutocompleteControl = new FormControl('');
    workloadFilteredOptions!: Observable<string[]>;

    files: any = [];

    constructor(
        private sessionService: SessionService, 
        private workloadService: WorkloadService,
        private activatedRoute: ActivatedRoute, 
        private location: Location
    ) { }

    ngOnInit() {

        this.activatedRoute.paramMap.subscribe(params => {
            
            let idParam: string | null = params.get('id');
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.sessionService.getSession(id).subscribe(session => {
                    this.session = session;
                })

                this.workloadService.getWorkloadsFromSession(id).subscribe(workloads => {
                    this.workloads = workloads;
                    this.workloadFilteredOptions = this.workloadAutocompleteControl.valueChanges.pipe(
                        startWith(''),
                        map(value => this.workloads
                            .filter(workload => (workload.workload_name || '').toLowerCase().includes((value || '').toLowerCase()))
                            .map(workload => `${workload.workload_name} (#${workload.id})`)
                        )
                    );
                })
            }                
        })
    }

    saveSession() {

        if(this.files === null || this.files.length === 0) {
            this._snackBar.open("Please select at least one file to upload!", '', { duration: 3000 });
            return;
        }

        let currWorkload: Workload | null = this.workloads.find(w => `${w.workload_name} (#${w.id})` === this.selectedWorkload) || null;

        this.sessionService.uploadSessionFiles(this.session, currWorkload, this.files).subscribe(response => {
            this._snackBar.open("Session files uploaded successfully!", '', { duration: 3000 });
            this.back();
        });
    }

    onFileSelected(e: any) {

        this.files = [];
        for (let file of e.target.files) {
            this.files.push(file);
            this.currFileNames += (this.currFileNames ? ', ' : '') + file.name;
        }
    }

    back() {
        this.location.back();
    }
}