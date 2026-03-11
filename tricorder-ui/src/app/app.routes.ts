import { Routes } from '@angular/router';
import { ApplicationListComponent } from './application/application-list/application-list';
import { ApplicationFormComponent } from './application/application-form/application-form';
import { HomeComponent } from './home/home';
import { ArtifactListComponent } from './artifact/artifact-list/artifact-list';
import { ArtifactFormComponent } from './artifact/artifact-form/artifact-form';
import { WorkloadFormComponent } from './workload/workload-form/workload-form';
import { WorkloadListComponent } from './workload/workload-list/workload-list';
import { SessionFormComponent } from './session/session-form/session-form';
import { SessionListComponent } from './session/session-list/session-list';
import { SessionReportComponent } from './session/session-report/session-report';
import { SessionUploadComponent } from './session/session-upload/session-upload';

export const routes: Routes = [
    
    { path: 'home', component: HomeComponent },
    { path: '', redirectTo: '/home', pathMatch: 'full' },

    /* APPLICATION PATHS */
    { path: 'projects', component: ApplicationListComponent },
    { path: 'project/:id/view', component: ApplicationFormComponent },
    { path: 'project/:id/edit', component: ApplicationFormComponent },
    { path: 'project/new', component: ApplicationFormComponent },
    { 
        path: 'project/:id', 
        redirectTo: ({params}) => {
            const appId = params['id'];
            return `/project/${appId}/view`;
        },
        pathMatch: 'full'
    },

    /* ARTIFACT PATHS */
    { path: 'versions', component: ArtifactListComponent },
    { path: 'version/:id/view', component: ArtifactFormComponent },
    { path: 'version/:id/edit', component: ArtifactFormComponent },
    { path: 'version/new', component: ArtifactFormComponent },
    {
        path: 'version/:id',
        redirectTo: ({params}) => {
            const artifactId = params['id'];
            return `/version/${artifactId}/view`;
        },
        pathMatch: 'full'
    },

    /* WORKLOAD PATHS */
    { path: 'workloads', component: WorkloadListComponent },
    { path: 'workload/:id/view', component: WorkloadFormComponent },
    { path: 'workload/:id/edit', component: WorkloadFormComponent },
    { path: 'workload/:application_id/new', component: WorkloadFormComponent },
    { path: 'workload/new', component: WorkloadFormComponent },
    {
        path: 'workload/:id',
        redirectTo: ({params}) => {
            const workloadId = params['id'];
            return `/workload/${workloadId}/view`;
        },
        pathMatch: 'full'
    },

    /* SESSION PATHS */
    { path: 'sessions', component: SessionListComponent },
    { path: 'session/:id/report', component: SessionReportComponent },
    { path: 'session/:id/upload', component: SessionUploadComponent },
    { path: 'session/:id/view', component: SessionFormComponent },
    { path: 'session/:id/edit', component: SessionFormComponent },
    { path: 'session/new', component: SessionFormComponent },
    {
        path: 'session/:id',
        redirectTo: ({params}) => {
            const sessionId = params['id'];
            return `/session/${sessionId}/view`;
        },
        pathMatch: 'full'
    }
];
