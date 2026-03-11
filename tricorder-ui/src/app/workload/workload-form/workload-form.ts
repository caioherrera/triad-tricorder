import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Workload, WorkloadService } from '../../../services/workload-service';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatGridListModule } from '@angular/material/grid-list';
import { CommonModule, Location } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { Application, ApplicationService } from '../../../services/application-service';
import { Observable, startWith } from 'rxjs';
import { map } from 'rxjs/operators';

@Component({
  selector: 'workload-form',
  imports: [ CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule, 
    MatCheckboxModule, MatAutocompleteModule, ReactiveFormsModule ],
  templateUrl: './workload-form.html',
  styleUrls: ['../../../styles.scss', './workload-form.scss']
})
export class WorkloadFormComponent { 

    private _snackBar = inject(MatSnackBar);
    private readonly _router = inject(Router);

    autocompleteControl = new FormControl('');
    filteredOptions!: Observable<string[]>;

    applications: Application[] = [];
    workload: Workload = new Workload();
    selectedApplication: string = "";

    mode!: string
    pageTitle: string = "Workload view"

    isNewRegister: boolean = true;
    isReadOnly: boolean = true;

    constructor(private workloadService: WorkloadService, private applicationService: ApplicationService, private activatedRoute: ActivatedRoute, private location: Location) { }

    ngOnInit() {

        this.activatedRoute.url.subscribe(urlParts => {
            this.mode = urlParts[urlParts.length - 1].path;
            this.isReadOnly = this.mode === "view";
            this.isNewRegister = this.mode === "new";
            
            this.isReadOnly ? this.autocompleteControl.disable() : this.autocompleteControl.enable();

            switch(this.mode) {
                case 'new':
                    this.pageTitle = 'Register new workload';
                    break;
                case 'edit':
                    this.pageTitle = 'Edit workload';
                    break;
                default:
                    this.pageTitle = 'View workload';
                    break;
            }
        })

        this.activatedRoute.paramMap.subscribe(params => {
            
            let idParam: string | null = params.get('id');
            let appIdParam: string | null = params.get('application_id');
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.workloadService.getWorkload(id).subscribe(workload => {
                    this.workload = workload;
                    this.selectedApplication = `${this.workload.application?.application_name} (#${this.workload.application?.id})`;
                })
            }
            else if(appIdParam !== null) {
                let id = Number(appIdParam);

                this.applicationService.getApplication(id).subscribe(application => {
                    this.selectedApplication = `${application.application_name} (#${application.id})`;
                })
            }

            this.applicationService.getApplications().subscribe(applications => {
                
                this.applications = applications;
                
                this.filteredOptions = this.autocompleteControl.valueChanges.pipe(
                    startWith(''),
                    map(value => this.applications
                        .filter(app => (app.application_name || '').toLowerCase().includes((value || '').toLowerCase()))
                        .map(app => `${app.application_name} (#${app.id})`))
                );
            })

        })
    }

    saveWorkload() {

        this.workload.application = this.applications.filter(app => `${app.application_name} (#${app.id})`.toLowerCase() == this.selectedApplication.toLowerCase())[0];

        this.workloadService.upsertWorkload(this.workload).subscribe(workload => {
            this.workload = workload;
            this._snackBar.open("Workload saved succesfully!", '', { duration: 3000 });
            this.back();
        })
    }

    back() {
        this.location.back();
    }
}
