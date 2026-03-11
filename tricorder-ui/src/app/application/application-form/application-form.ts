import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Application, ApplicationService } from '../../../services/application-service';
import { Artifact, ArtifactService } from '../../../services/artifact-service';
import { Workload, WorkloadService } from '../../../services/workload-service';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatGridListModule } from '@angular/material/grid-list';
import { CommonModule, Location } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { config } from 'process';

@Component({
  selector: 'application-form',
  imports: [CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule, RouterLink, RouterLinkActive ],
  templateUrl: './application-form.html',
  styleUrls: ['../../../styles.scss', './application-form.scss']
})
export class ApplicationFormComponent { 

    private _snackBar = inject(MatSnackBar);
    private readonly _router = inject(Router);

    application: Application = new Application();
    reference_artifact: Artifact = new Artifact();
    workloads: Workload[] = [];
    
    mode!: string
    pageTitle: string = "Application view"

    isNewRegister: boolean = true;
    isReadOnly: boolean = true;

    columnLabels: string[] = ["id", "name", "description", "input_value", "actions"]

    constructor(private applicationService: ApplicationService, private artifactService: ArtifactService, private workloadService: WorkloadService, private activatedRoute: ActivatedRoute, private location: Location) { }

    ngOnInit() {

        this.activatedRoute.url.subscribe(urlParts => {
            this.mode = urlParts[urlParts.length - 1].path;
            this.isReadOnly = this.mode === "view";
            this.isNewRegister = this.mode === "new";
            
            switch(this.mode) {
                case 'new':
                    this.pageTitle = 'Register new project';
                    break;
                case 'edit':
                    this.pageTitle = 'Edit project';
                    break;
                default:
                    this.pageTitle = 'View project';
                    break;
            }
        })

        this.activatedRoute.paramMap.subscribe(params => {
            
            let idParam: string | null = params.get('id'); 
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.applicationService.getApplication(id).subscribe(app => {
                    this.application = app;
                })
                this.artifactService.getReferenceArtifact(id).subscribe(artifact => {
                    this.reference_artifact = artifact;
                })
                this.workloadService.getApplicationWorkloads(id).subscribe(workloads => {
                    this.workloads = workloads;
                })
            }
        })
    }

    saveApplication() {

        this.applicationService.upsertApplication(this.application).subscribe(app => {
            this.application = app;
            this._snackBar.open("Project saved succesfully!", '', { duration: 3000 });
            this.back();
        })
    }

    back() {
        this.location.back();
    }
}
