import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Artifact, ArtifactService } from '../../../services/artifact-service';
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
  selector: 'artifact-form',
  imports: [ CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule,
    MatCheckboxModule, MatAutocompleteModule, ReactiveFormsModule ],
  templateUrl: './artifact-form.html',
  styleUrls: ['../../../styles.scss', './artifact-form.scss']
})
export class ArtifactFormComponent { 

    private _snackBar = inject(MatSnackBar);
    private readonly _router = inject(Router);

    autocompleteControl = new FormControl('');
    filteredOptions!: Observable<string[]>;

    applications: Application[] = [];
    artifact: Artifact = new Artifact();
    selectedApplication: string = "";

    mode!: string
    pageTitle: string = "Artifact view"

    isNewRegister: boolean = true;
    isReadOnly: boolean = true;

    constructor(private artifactService: ArtifactService, private applicationService: ApplicationService, private activatedRoute: ActivatedRoute, private location: Location) { }

    ngOnInit() {

        this.activatedRoute.url.subscribe(urlParts => {
            this.mode = urlParts[urlParts.length - 1].path;
            this.isReadOnly = this.mode === "view";
            this.isNewRegister = this.mode === "new";
            
            this.isReadOnly ? this.autocompleteControl.disable() : this.autocompleteControl.enable();

            switch(this.mode) {
                case 'new':
                    this.pageTitle = 'Register new version';
                    break;
                case 'edit':
                    this.pageTitle = 'Edit version';
                    break;
                default:
                    this.pageTitle = 'View version';
                    break;
            }
        })

        this.activatedRoute.paramMap.subscribe(params => {
            
            let idParam: string | null = params.get('id'); 
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.artifactService.getArtifact(id).subscribe(artifact => {
                    this.artifact = artifact;
                    this.selectedApplication = `${this.artifact.application?.application_name} (#${this.artifact.application?.id})`;
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

    saveArtifact() {

        this.artifact.application = this.applications.filter(app => `${app.application_name} (#${app.id})`.toLowerCase() == this.selectedApplication.toLowerCase())[0];

        this.artifactService.upsertArtifact(this.artifact).subscribe(artifact => {
            this.artifact = artifact;
            this._snackBar.open("Version saved succesfully!", '', { duration: 3000 });
            this.back();
        })
    }

    back() {
        this.location.back();
    }
}
