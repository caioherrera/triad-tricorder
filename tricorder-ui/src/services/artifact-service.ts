import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Application } from "./application-service";
import { environment } from '../environments/environment';

const base_url = environment.backendBaseUrl;

const applications_api: string = base_url + '/api/applications';
const artifacts_api: string = base_url + '/api/artifacts';
const single_artifacts_api: string = artifacts_api + '/<artifact_id>';
const artifacts_from_application_api: string = applications_api + '/<application_id>/artifacts';
const reference_artifacts_from_application_api: string = applications_api + '/<application_id>/reference_artifact';

const save_artifact_api: string = artifacts_api + '/upsert';

export class Artifact {

    id: number | null = null;
    artifact_name: string | null = null;
    application: Application | null = null;
    is_reference: number | null = null;
    file_path: string | null = null;
}

@Injectable({providedIn: "root"})
export class ArtifactService {
    
    constructor(private http: HttpClient) { }

    getArtifacts(): Observable<Artifact[]> {

        return this.http.get<Artifact[]>(artifacts_api);
    }

    getArtifact(id: number): Observable<Artifact> {

        let url: string = single_artifacts_api.replace("<artifact_id>", id.toString());

        return this.http.get<Artifact>(url);
    }

    getArtifactsForApplication(application_id: number): Observable<Artifact[]> {

        let url: string = artifacts_from_application_api.replace("<application_id>", application_id.toString());

        return this.http.get<Artifact[]>(url);
    }

    getReferenceArtifact(application_id: number): Observable<Artifact> {

        let url: string = reference_artifacts_from_application_api.replace("<application_id>", application_id.toString());

        return this.http.get<Artifact>(url);
    }

    upsertArtifact(artifact: Artifact): Observable<Artifact> {
        let url: string = save_artifact_api;
        return this.http.post<Artifact>(url, artifact);   
    }
}