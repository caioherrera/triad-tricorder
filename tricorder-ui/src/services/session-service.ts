import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { Artifact } from "./artifact-service";
import { Workload } from "./workload-service";
import { environment } from '../environments/environment';

const base_url = environment.backendBaseUrl;

const applications_api: string = base_url + '/api/applications';
const sessions_api: string = base_url + '/api/sessions';
const single_sessions_api: string = sessions_api + '/<session_id>';
const sessions_from_application_api: string = applications_api + '/<application_id>/sessions';
const session_monitor_api: string = single_sessions_api + '/monitor';
const session_analysis_api: string = single_sessions_api + '/analyze';
const session_full_process_api: string = single_sessions_api + '/full_process';
const session_details_api: string = single_sessions_api + '/details';
const session_upload_api: string = single_sessions_api + '/workload/<workload_id>/upload';

const save_session_api: string = sessions_api + '/upsert';

export class Session {
    id: number | null = null;
    artifact: Artifact | null = null;
    session_type: string | null = null;
    num_executions: number | null = null;
    sample_interval: number | null = null;
    sample_count: number | null = null;
    reference_session: Session | null = null;
    status: string | null = null;
    continuous_execution: boolean | null = null;
    restrictive: boolean | null = null;
}

export class SessionWorkload {
    id: number | null = null;
    session: Session | null = null;
    workload: Workload | null = null;
    monitoring_status: string | null = null;
    analysis_status: string | null = null;
    monitoring_start_time_seconds: string | null = null;
    monitoring_end_time_seconds: string | null = null;
    analysis_start_time_seconds: string | null = null;
    analysis_end_time_seconds: string | null = null;
    monitoring_elapsed_time: string | null = null;
    analysis_elapsed_time: string | null = null;
    verdict: number | null = null;
    text_verdict: string | null = null; 
    iterations_to_detect: number | null = null;
    total_iterations: number | null = null;
}

@Injectable({providedIn: "root"})
export class SessionService {
    
    constructor(private http: HttpClient) { }

    getSessions(): Observable<Session[]> {

        return this.http.get<Session[]>(sessions_api);
    }

    getSession(id: number): Observable<Session> {
        
        let url: string = single_sessions_api.replace("<session_id>", id.toString());
        return this.http.get<Session>(url);
    }

    getSessionsForApplication(application_id: number): Observable<Session[]> {

        let url: string = sessions_from_application_api.replace("<application_id>", application_id.toString());

        return this.http.get<Session[]>(url);
    }

    getSessionDetails(id: number): Observable<SessionWorkload[]> {
        let url: string = session_details_api.replace("<session_id>", id.toString());
        return this.http.get<SessionWorkload[]>(url);
    }

    upsertSession(session: Session, workloads: Workload[] = []): Observable<Session> {

        let url: string = save_session_api;
        if(workloads.length > 0) {
            return this.http.post<Session>(url, {session: session, workloads: workloads});
        }

        return this.http.post<Session>(url, session);   
    }

    uploadSessionFiles(session: Session, workload: Workload | null, files: File[] = []): Observable<any> {

        let formData: FormData = new FormData();
        for (const file of files) {
            formData.append('files', file, file.name);
        }

        let url: string = session_upload_api.replace("<session_id>", (session.id || '').toString()).replace("<workload_id>", (workload?.id || '').toString());
        return this.http.post<any>(url, formData);
    }

    startMonitor(id: number): Observable<Session> {

        let url: string = session_monitor_api.replace("<session_id>", id.toString());
        return this.http.get<Session>(url);
    }

    startAnalysis(id: number): Observable<Session> {
        let url: string = session_analysis_api.replace("<session_id>", id.toString());
        return this.http.get<Session>(url);
    }

    startFullProcess(id: number): Observable<Session> {
        let url: string = session_full_process_api.replace("<session_id>", id.toString());
        return this.http.get<Session>(url);
    }
}