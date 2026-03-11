import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router, RouterLink, RouterLinkActive } from '@angular/router';
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
import { Observable, startWith } from 'rxjs';
import { map } from 'rxjs/operators';
import { Artifact, ArtifactService } from '../../../services/artifact-service';
import { Application, ApplicationService } from '../../../services/application-service';
import { MatSelectModule } from '@angular/material/select';
import { Workload, WorkloadService } from '../../../services/workload-service';

@Component({
  selector: 'session-form',
  imports: [ CommonModule, MatInputModule, MatFormFieldModule, FormsModule, MatIconModule, MatGridListModule, MatTableModule,
    MatCheckboxModule, MatAutocompleteModule, ReactiveFormsModule, MatSelectModule, MatListModule, RouterLink, RouterLinkActive ],
  templateUrl: './session-form.html',
  styleUrls: ['../../../styles.scss', './session-form.scss']
})
export class SessionFormComponent { 

    private _snackBar = inject(MatSnackBar);
    private readonly _router = inject(Router);

    applications: Application[] = [];
    selectedApplication: string = "";
    applicationAutocompleteControl = new FormControl('');
    applicationFilteredOptions!: Observable<string[]>;

    artifacts: Artifact[] = [];
    selectedArtifact: string = "";
    artifactAutocompleteControl = new FormControl('');
    artifactFilteredOptions!: Observable<string[]>;

    workloads: Workload[] = [];
    selectedWorkloads: number[] = [];

    referenceSessions: Session[] = [];
    selectedRefSession: string = "";
    refSessionAutocompleteControl = new FormControl('');
    refSessionFilteredOptions!: Observable<string[]>;
    
    session: Session = new Session();

    sessionTypeCanReference: any = {
        "training": null,
        "validation": "training",
        "test": "training"
    }

    mode!: string
    pageTitle: string = "Session view"

    isNewRegister: boolean = true;
    isReadOnly: boolean = true;

    constructor(
        private applicationService: ApplicationService, 
        private artifactService: ArtifactService, 
        private sessionService: SessionService, 
        private workloadService: WorkloadService,
        private activatedRoute: ActivatedRoute, 
        private location: Location
    ) { }

    ngOnInit() {

        this.activatedRoute.url.subscribe(urlParts => {
            this.mode = urlParts[urlParts.length - 1].path;
            this.isReadOnly = this.mode === "view";
            this.isNewRegister = this.mode === "new";
            
            if(this.isReadOnly) {
                this.artifactAutocompleteControl.disable();
                this.applicationAutocompleteControl.disable();
                this.refSessionAutocompleteControl.disable();
            } 
            else {
                this.artifactAutocompleteControl.enable();
                this.applicationAutocompleteControl.enable();
                this.refSessionAutocompleteControl.enable();
            }

            switch(this.mode) {
                case 'new':
                    this.pageTitle = 'Register new session';
                    break;
                case 'edit':
                    this.pageTitle = 'Edit session';
                    break;
                default:
                    this.pageTitle = 'View session';
                    break;
            }
        })

        this.activatedRoute.paramMap.subscribe(params => {
            
            let idParam: string | null = params.get('id');
            
            if(idParam !== null) {
                let id = Number(idParam);

                this.sessionService.getSession(id).subscribe(session => {
                    this.session = session;
                    this.selectedApplication = `${this.session.artifact?.application?.application_name} (#${this.session.artifact?.application?.id})`;
                    this.selectedArtifact = `${this.session.artifact?.artifact_name} (#${this.session.artifact?.id})`;
                    
                    let selectedRefSession: string = this.session.reference_session 
                        ? `${this.session.reference_session?.session_type?.charAt(0).toUpperCase()}${this.session.reference_session?.session_type?.slice(1)} (#${this.session.reference_session?.id})`
                        : "";

                    this.selectedRefSession = selectedRefSession;

                    if(this.session.artifact?.application?.id) {
                        this.generateArtifactList(this.session.artifact?.application?.id);
                        this.generateRefSessionList(this.session.artifact?.application?.id);
                        this.generateWorkloadList(this.session.artifact?.application?.id);
                    }

                    this.workloadService.getWorkloadsFromSession(id).subscribe(workloads => {
                        this.selectedWorkloads = workloads.map(workload => workload.id) as number[];
                        console.log("initially selected workloads: ", this.selectedWorkloads);
                    });

                })
            }

            this.generateApplicationList();                
        })
    }

    filterOptions() {

        this.selectedArtifact = "";
        this.selectedRefSession = "";
        let currApplication: Application = this.applications.filter(app => `${app.application_name} (#${app.id})` == this.selectedApplication)[0];

        if(currApplication && currApplication.id) {
            this.generateArtifactList(currApplication.id);
            this.generateRefSessionList(currApplication.id);
            this.generateWorkloadList(currApplication.id);
        }        
    }

    generateApplicationList() {
        this.applicationService.getApplications().subscribe(applications => {
            this.applications = applications;
            this.applicationFilteredOptions = this.applicationAutocompleteControl.valueChanges.pipe(
                startWith(''),
                map(value => this.applications
                    .filter(app => (app.application_name || '').toLowerCase().includes((value || '').toLowerCase()))
                    .map(app => `${app.application_name} (#${app.id})`)
                )
            );
        })
    }

    generateArtifactList(applicationId: number) {
        this.artifactService.getArtifactsForApplication(applicationId).subscribe(artifacts => {
            this.artifacts = artifacts;
            this.artifactFilteredOptions = this.artifactAutocompleteControl.valueChanges.pipe(
                startWith(''),
                map(value => this.artifacts
                    .filter(artifact => (artifact.artifact_name || '').toLowerCase().includes((value || '').toLowerCase()))
                    .map(artifact => `${artifact.artifact_name} (#${artifact.id})`)
                )
            )
        })
    }

    generateRefSessionList(applicationId: number) {
        this.sessionService.getSessionsForApplication(applicationId).subscribe(sessions => {
            this.referenceSessions = sessions
                .filter(session => { return !this.session.id || session.id != this.session.id })
                .filter(session => { return !this.session.session_type || session.session_type == this.sessionTypeCanReference[this.session.session_type] })
            this.refSessionFilteredOptions = this.refSessionAutocompleteControl.valueChanges.pipe(
                startWith(''),
                map(value => this.referenceSessions
                    .filter(session => (session.session_type || '').toLowerCase().includes((value || '').toLowerCase()))
                    .map(session => `${session.session_type} (#${session.id})`)
                )
            )
        })
    }

    generateWorkloadList(applicationId: number) {
        this.workloadService.getApplicationWorkloads(applicationId).subscribe(workloads => {
            this.workloads = workloads;
            console.log("workloads: ", workloads);
        })
    }

    startSessionMonitor() {
        this.sessionService.startMonitor(this.session.id as number).subscribe(session => {
            this._snackBar.open("Session monitoring started!", '', { duration: 3000});
            this.back();
        })
    }

    startSessionAnalysis() {
        this.sessionService.startAnalysis(this.session.id as number).subscribe(session => {
            this._snackBar.open("Session analysis started!", '', { duration: 3000});
            this.back();
        })
    }

    startSessionFullProcess() {
        this.sessionService.startFullProcess(this.session.id as number).subscribe(session => {
            this._snackBar.open("Session full process started!", '', { duration: 3000});
            this.back();
        })
    }

    saveSession() {

        this.session.artifact = this.artifacts.filter(artifact => `${artifact.artifact_name} (#${artifact.id})` == this.selectedArtifact)[0];
        
        if(this.selectedRefSession !== null) {
            this.session.reference_session = this.referenceSessions.filter(session => `${session.session_type} (#${session.id})`.toLowerCase() == this.selectedRefSession.toLowerCase())[0] || null;
        }
        
        let workloadsToSSave = this.workloads.filter(workload => this.selectedWorkloads.includes(workload.id as number));
        this.sessionService.upsertSession(this.session, workloadsToSSave).subscribe(session => {
            this.session = session;
            this._snackBar.open("Session saved succesfully!", '', { duration: 3000 });
            this.back();
        })
    }

    back() {
        this.location.back();
    }

    hideMonitorButton() {
        return this.session.status != 'not_started';
    }

    hideAnalysisButton() {
        return this.session.status != 'monitoring_completed' && this.session.status != 'manual_monitoring';
    }

    hideRunFullButton() {
        return this.session.status != 'not_started';
    }

    hideReportButton() {
        return this.session.status == 'not_started';
    }

    hideUploadButton() {
        return this.session.status != 'not_started' && this.session.status != 'manual_monitoring';
    }
}
